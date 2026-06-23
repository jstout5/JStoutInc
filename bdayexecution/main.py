"""
B Day Execution — FastAPI backend
Routes:
  POST /subscribe        — receives form from bday.html, stores in DB
  GET  /approve/{id}     — JStout clicks this in email to trigger purchase
  POST /webhook/stripe   — Stripe calls this on payment success
  GET  /admin            — Quick dashboard of all subscribers + upcoming
"""
import asyncio
import base64
import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Form, Request, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from db import (
    init_db, add_subscriber, add_recipient,
    activate_subscriber, approve_order, get_order, mark_purchased, get_conn,
    get_products, add_product, delete_product, toggle_product_stock
)

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "jstout2025")
from scheduler import start_scheduler
from walmart import purchase_gift
from emailer import send_subscriber_confirmation, send_shipped_notice

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

STRIPE_CHECKOUT = "https://buy.stripe.com/4gM4gsfrn4Ar5T19lr5Rm00"


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    scheduler = start_scheduler()
    yield
    scheduler.shutdown()

app = FastAPI(title="B Day Execution", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://jstoutinc.onrender.com", "http://localhost", "file://"],
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)

def require_admin(key: str = ""):
    if key != ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="Forbidden")


# ── SUBSCRIBE ─────────────────────────────────────────────────────────────────

@app.post("/subscribe")
async def subscribe(
    email:            str = Form(...),
    recipient_name:   str = Form(...),
    gender:           str = Form(...),
    birthday:         str = Form(...),
    gift_budget:      str = Form(...),
    shipping_name:    str = Form(...),
    shipping_address: str = Form(...),
):
    sub_id = add_subscriber(email, shipping_name, shipping_address)
    rec_id, is_dupe = add_recipient(sub_id, recipient_name, gender, birthday, gift_budget)

    if is_dupe:
        return HTMLResponse(content=_dupe_page(recipient_name), status_code=200)

    # Send confirmation and redirect to Stripe
    try:
        send_subscriber_confirmation(email, recipient_name, birthday)
    except Exception as e:
        log.warning(f"Confirmation email failed: {e}")

    return RedirectResponse(STRIPE_CHECKOUT, status_code=303)


# ── STRIPE WEBHOOK ─────────────────────────────────────────────────────────────

@app.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    payload = await request.json()
    event_type = payload.get("type", "")

    if event_type == "checkout.session.completed":
        email = payload.get("data", {}).get("object", {}).get("customer_details", {}).get("email")
        if email:
            activate_subscriber(email)
            log.info(f"Activated subscriber: {email}")

    return {"ok": True}


# ── APPROVE + PURCHASE ─────────────────────────────────────────────────────────

@app.get("/approve/{order_id}")
async def approve(order_id: int):
    order = get_order(order_id)
    if not order:
        raise HTTPException(404, "Order not found")

    approve_order(order_id)

    # Kick off purchase in background so the email click returns fast
    asyncio.create_task(_do_purchase(order_id, order))

    return HTMLResponse(content=f"""
    <html><body style="font-family:Arial;text-align:center;padding:60px">
      <h1 style="color:#16a34a">✅ Approved!</h1>
      <p>Purchasing the gift for <strong>{order['name']}</strong> now.<br>
      You'll get a shipped confirmation email when the order is placed.</p>
    </body></html>
    """)


async def _do_purchase(order_id: int, order: dict):
    try:
        walmart_id = await purchase_gift(
            product_url=order["product_url"],
            shipping_name=order["shipping_name"],
            shipping_address=order["shipping_address"],
        )
        mark_purchased(order_id, walmart_id)
        log.info(f"Order {order_id} purchased. Walmart ID: {walmart_id}")

        # Email subscriber
        with get_conn() as conn:
            sub = conn.execute(
                "SELECT s.email FROM subscribers s "
                "JOIN recipients r ON r.subscriber_id=s.id "
                "JOIN orders o ON o.recipient_id=r.id WHERE o.id=?",
                (order_id,)
            ).fetchone()
            if sub:
                send_shipped_notice(sub["email"], order["name"], walmart_id)

    except Exception as e:
        log.error(f"Purchase failed for order {order_id}: {e}")


# ── ADMIN DASHBOARD ────────────────────────────────────────────────────────────

@app.get("/admin", response_class=HTMLResponse)
async def admin():
    from db import get_upcoming_birthdays
    upcoming = get_upcoming_birthdays(9)

    with get_conn() as conn:
        subs  = conn.execute("SELECT COUNT(*) as c FROM subscribers WHERE active=1").fetchone()["c"]
        recs  = conn.execute("SELECT COUNT(*) as c FROM recipients").fetchone()["c"]
        orders = conn.execute("SELECT COUNT(*) as c FROM orders WHERE status='purchased'").fetchone()["c"]
        recent = conn.execute(
            "SELECT o.id, r.name, o.product_name, o.product_price, o.status, o.created_at "
            "FROM orders o JOIN recipients r ON r.id=o.recipient_id "
            "ORDER BY o.created_at DESC LIMIT 20"
        ).fetchall()

    rows = "".join(
        f"<tr><td>{r['id']}</td><td>{r['name']}</td><td>{(r['product_name'] or '')[:50]}</td>"
        f"<td>${r['product_price'] or 0:.2f}</td><td>{r['status']}</td><td>{r['created_at']}</td></tr>"
        for r in recent
    )
    up_rows = "".join(
        f"<tr><td>{r['name']}</td><td>{r['gender']}</td><td>{r['birthday']}</td>"
        f"<td>{r['gift_budget']}</td><td>{r['sub_email']}</td></tr>"
        for r in upcoming
    )

    return f"""<html><head><title>B Day Admin</title>
    <style>body{{font-family:Arial;padding:24px}}table{{border-collapse:collapse;width:100%;margin-top:12px}}
    th,td{{border:1px solid #ddd;padding:8px;text-align:left;font-size:13px}}th{{background:#f0eadb}}
    .stat{{display:inline-block;background:#fff;border:1px solid #ddd;border-radius:8px;padding:16px 24px;margin:8px;text-align:center}}
    .stat-n{{font-size:32px;font-weight:900;color:#c8102e}}.stat-l{{font-size:12px;color:#888}}</style>
    </head><body>
    <h1 style="color:#c8102e">🎁 B Day Execution — Admin</h1>
    <div class="stat"><div class="stat-n">{subs}</div><div class="stat-l">Active Subscribers</div></div>
    <div class="stat"><div class="stat-n">{recs}</div><div class="stat-l">Recipients</div></div>
    <div class="stat"><div class="stat-n">{orders}</div><div class="stat-l">Gifts Purchased</div></div>
    <h2 style="margin-top:24px">⚠️ Upcoming (9 days)</h2>
    <table><tr><th>Name</th><th>Gender</th><th>Birthday</th><th>Budget</th><th>Subscriber</th></tr>{up_rows}</table>
    <h2 style="margin-top:24px">Recent Orders</h2>
    <table><tr><th>ID</th><th>Recipient</th><th>Product</th><th>Price</th><th>Status</th><th>Created</th></tr>{rows}</table>
    </body></html>"""


# ── PUBLIC PRODUCTS API ────────────────────────────────────────────────────────

@app.get("/api/products")
async def api_products():
    return JSONResponse(get_products())


# ── ADMIN SHOP ─────────────────────────────────────────────────────────────────

@app.get("/admin/shop", response_class=HTMLResponse)
async def admin_shop(key: str = ""):
    if key != ADMIN_PASSWORD:
        return HTMLResponse(_admin_login("shop"))
    products = get_products()
    rows = ""
    for p in products:
        img = f'<img src="{p["image_b64"]}" style="height:50px;border-radius:4px">' if p.get("image_b64") else "—"
        stock = "✅ In Stock" if p["in_stock"] else "❌ Out"
        rows += f"""<tr>
          <td>{img}</td>
          <td><strong>{p['name']}</strong><br><small style="color:#888">{p['description'] or ''}</small></td>
          <td><strong>${p['price']:,.2f}</strong></td>
          <td>{stock}</td>
          <td>
            <form method="POST" action="/admin/shop/{p['id']}/toggle?key={key}" style="display:inline">
              <button style="{_btn_style('#555')}">Toggle Stock</button>
            </form>
            <form method="POST" action="/admin/shop/{p['id']}/delete?key={key}" style="display:inline"
                  onsubmit="return confirm('Delete this product?')">
              <button style="{_btn_style('#c8102e')}">Delete</button>
            </form>
          </td>
        </tr>"""

    return f"""<!DOCTYPE html><html><head><title>Shop Admin — JStout Inc</title>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <style>
      body{{font-family:'Segoe UI',sans-serif;background:#f5f0e8;margin:0;padding:24px;}}
      h1{{color:#c8102e;margin-bottom:4px;}} .sub{{color:#888;font-size:13px;margin-bottom:28px;}}
      .card{{background:#fff;border-radius:12px;padding:24px;box-shadow:0 2px 12px rgba(0,0,0,.08);margin-bottom:24px;}}
      table{{width:100%;border-collapse:collapse;}} th,td{{padding:10px 12px;border-bottom:1px solid #eee;text-align:left;font-size:13px;}}
      th{{background:#f9f6f0;font-weight:700;color:#555;}}
      label{{display:block;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#888;margin-bottom:5px;margin-top:14px;}}
      input,textarea,select{{width:100%;padding:10px 12px;border:1.5px solid #ddd;border-radius:7px;font-size:14px;outline:none;}}
      input:focus,textarea:focus{{border-color:#c8102e;}}
      .grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px;}}
    </style></head><body>
    <h1>🛍️ Shop Admin</h1>
    <div class="sub">JStout Inc — Product Management &nbsp;|&nbsp; <a href="/admin?key={key}">← B Day Dashboard</a></div>

    <div class="card">
      <h3 style="margin-bottom:16px">Add New Product</h3>
      <form method="POST" action="/admin/shop/add?key={key}" enctype="multipart/form-data">
        <label>Product Name</label>
        <input name="name" required placeholder="e.g. Cactus Jack 2025 NBA Hobby Box">
        <label>Description</label>
        <textarea name="description" rows="2" placeholder="Factory Sealed · Ships Insured"></textarea>
        <div class="grid">
          <div><label>Price ($)</label><input name="price" type="number" step="0.01" required placeholder="1000.00"></div>
          <div><label>Product Image</label><input name="image" type="file" accept="image/*"></div>
        </div>
        <div class="grid">
          <div><label>PayPal Link</label><input name="paypal_link" placeholder="https://paypal.com/..."></div>
          <div><label>Stripe Link</label><input name="stripe_link" placeholder="https://buy.stripe.com/..."></div>
        </div>
        <button type="submit" style="{_btn_style('#c8102e')};margin-top:18px;padding:12px 24px;font-size:13px;">
          ➕ Add Product
        </button>
      </form>
    </div>

    <div class="card">
      <h3 style="margin-bottom:16px">Current Products ({len(products)})</h3>
      <table>
        <tr><th>Image</th><th>Product</th><th>Price</th><th>Stock</th><th>Actions</th></tr>
        {rows if rows else '<tr><td colspan="5" style="text-align:center;color:#aaa;padding:24px">No products yet</td></tr>'}
      </table>
    </div>
    </body></html>"""


@app.post("/admin/shop/add", response_class=HTMLResponse)
async def admin_add_product(
    key: str = "",
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    paypal_link: str = Form(""),
    stripe_link: str = Form(""),
    image: UploadFile = File(None),
):
    require_admin(key)
    image_b64 = None
    if image and image.filename:
        data = await image.read()
        ext = image.content_type or "image/jpeg"
        image_b64 = f"data:{ext};base64," + base64.b64encode(data).decode()
    add_product(name, description, price, image_b64, paypal_link or None, stripe_link or None)
    return RedirectResponse(f"/admin/shop?key={key}", status_code=303)


@app.post("/admin/shop/{product_id}/delete")
async def admin_delete_product(product_id: int, key: str = ""):
    require_admin(key)
    delete_product(product_id)
    return RedirectResponse(f"/admin/shop?key={key}", status_code=303)


@app.post("/admin/shop/{product_id}/toggle")
async def admin_toggle_product(product_id: int, key: str = ""):
    require_admin(key)
    toggle_product_stock(product_id)
    return RedirectResponse(f"/admin/shop?key={key}", status_code=303)


def _btn_style(color):
    return f"background:{color};color:#fff;border:none;padding:6px 12px;border-radius:5px;cursor:pointer;font-size:11px;font-weight:700;margin:2px"

def _admin_login(next_page):
    return f"""<!DOCTYPE html><html><head><title>Admin Login</title>
    <style>body{{font-family:'Segoe UI',sans-serif;background:#f5f0e8;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;}}
    .box{{background:#fff;padding:40px;border-radius:14px;box-shadow:0 4px 20px rgba(0,0,0,.1);width:320px;text-align:center;}}
    h2{{color:#c8102e;margin-bottom:4px;}} p{{color:#888;font-size:13px;margin-bottom:24px;}}
    input{{width:100%;padding:12px;border:1.5px solid #ddd;border-radius:7px;font-size:15px;box-sizing:border-box;outline:none;margin-bottom:14px;}}
    button{{width:100%;padding:13px;background:#c8102e;color:#fff;border:none;border-radius:7px;font-size:14px;font-weight:700;cursor:pointer;}}</style>
    </head><body><div class="box">
    <h2>🔒 Admin</h2><p>JStout Inc — Restricted</p>
    <form method="GET" action="/admin/{next_page}">
      <input type="password" name="key" placeholder="Enter password" autofocus>
      <button type="submit">Unlock</button>
    </form>
    </div></body></html>"""


# ── DUPLICATE PAGE ─────────────────────────────────────────────────────────────

def _dupe_page(name: str) -> str:
    return f"""<html><body style="font-family:Arial;text-align:center;padding:60px">
    <div style="max-width:440px;margin:0 auto;background:#fff;border-radius:16px;padding:40px;box-shadow:0 4px 20px rgba(0,0,0,.1)">
      <div style="font-size:48px">⚠️</div>
      <h2 style="color:#c8102e;margin:12px 0">Already Subscribed</h2>
      <p style="color:#555;line-height:1.6">
        You already have an active B Day Execution subscription for <strong>{name}</strong>.
        Only one subscription per recipient is allowed.
      </p>
      <a href="/bday.html" style="display:inline-block;margin-top:20px;background:#c8102e;color:#fff;
        padding:12px 28px;border-radius:8px;text-decoration:none;font-weight:700">
        Add a Different Person
      </a>
    </div>
    </body></html>"""

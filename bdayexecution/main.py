"""
B Day Execution — FastAPI backend
Routes:
  POST /subscribe        — receives form from bday.html, stores in DB
  GET  /approve/{id}     — JStout clicks this in email to trigger purchase
  POST /webhook/stripe   — Stripe calls this on payment success
  GET  /admin            — Quick dashboard of all subscribers + upcoming
"""
import asyncio
import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from dotenv import load_dotenv

load_dotenv()

from db import (
    init_db, add_subscriber, add_recipient,
    activate_subscriber, approve_order, get_order, mark_purchased, get_conn
)
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

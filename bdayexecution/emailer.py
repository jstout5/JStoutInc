import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_EMAIL    = os.getenv("SMTP_EMAIL", "frostbytehero@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
BASE_URL      = os.getenv("BASE_URL", "http://localhost:8000")


def _send(to: str, subject: str, html: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"B Day Execution <{SMTP_EMAIL}>"
    msg["To"]      = to
    msg.attach(MIMEText(html, "html"))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(SMTP_EMAIL, SMTP_PASSWORD)
        s.sendmail(SMTP_EMAIL, to, msg.as_string())


def send_approval_email(order_id: int, recipient: dict, gifts: list[dict]):
    """Emails JStout: here are the top picks, click to approve."""
    approve_url = f"{BASE_URL}/approve/{order_id}"

    gift_rows = ""
    for i, g in enumerate(gifts[:3], 1):
        gift_rows += f"""
        <tr style="background:{'#fff' if i%2 else '#fafafa'}">
          <td style="padding:12px;font-weight:600">{g['name'][:80]}</td>
          <td style="padding:12px;color:#c8102e;font-weight:700">${g['price']:.2f}</td>
          <td style="padding:12px;color:#888">{g.get('rating','—')}</td>
          <td style="padding:12px"><a href="{g['link']}" target="_blank" style="color:#0070ba">View</a></td>
        </tr>"""

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto">
      <div style="background:#c8102e;padding:20px;border-radius:8px 8px 0 0">
        <h1 style="color:#fff;margin:0;font-size:22px">🎁 Birthday Alert — Action Required</h1>
      </div>
      <div style="background:#fff;padding:28px;border:1px solid #eee;border-top:none">
        <p style="font-size:15px;color:#333">
          <strong>{recipient['name']}'s</strong> birthday is in <strong>9 days</strong>.<br>
          Budget: <strong>{recipient['gift_budget']}</strong> &nbsp;|&nbsp;
          Gender: <strong>{recipient['gender']}</strong><br>
          Ship to: <strong>{recipient['shipping_name']}</strong>, {recipient['shipping_address']}
        </p>
        <h3 style="color:#333;margin-top:24px">Top Gift Options</h3>
        <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;border:1px solid #eee;border-radius:6px">
          <tr style="background:#f5f5f5">
            <th style="padding:10px;text-align:left;font-size:12px">Product</th>
            <th style="padding:10px;text-align:left;font-size:12px">Price</th>
            <th style="padding:10px;text-align:left;font-size:12px">Rating</th>
            <th style="padding:10px;text-align:left;font-size:12px">Link</th>
          </tr>
          {gift_rows}
        </table>
        <div style="text-align:center;margin-top:28px">
          <a href="{approve_url}" style="display:inline-block;background:#c8102e;color:#fff;padding:14px 36px;border-radius:8px;text-decoration:none;font-weight:700;font-size:16px;letter-spacing:1px">
            ✅ APPROVE — BUY THE TOP PICK
          </a>
          <p style="color:#aaa;font-size:11px;margin-top:10px">
            Clicking will automatically purchase the #1 result from Walmart and ship to {recipient['shipping_name']}.
          </p>
        </div>
      </div>
    </div>"""

    _send(SMTP_EMAIL, f"🎁 Birthday Alert: {recipient['name']} — Approve Gift Purchase", html)


def send_subscriber_confirmation(to_email: str, recipient_name: str, birthday: str):
    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:560px;margin:0 auto">
      <div style="background:#c8102e;padding:20px;border-radius:8px 8px 0 0">
        <h1 style="color:#fff;margin:0">🎁 You're all set!</h1>
      </div>
      <div style="background:#fff;padding:28px;border:1px solid #eee;border-top:none">
        <p style="font-size:15px;color:#333">
          We've got <strong>{recipient_name}</strong> on the calendar for <strong>{birthday}</strong>.
        </p>
        <p style="color:#555;line-height:1.6">
          9 days before their birthday we'll find the perfect gift on Walmart,
          order it with gift wrap, and ship it straight to your door —
          arriving 3 days before the big day.
        </p>
        <p style="color:#555">You don't have to do a thing. We've got it.</p>
        <p style="margin-top:24px;color:#888;font-size:12px">
          Questions? Reply to this email or contact frostbytehero@gmail.com
        </p>
      </div>
    </div>"""

    _send(to_email, f"🎁 B Day Execution: {recipient_name} is on the calendar!", html)


def send_shipped_notice(to_email: str, recipient_name: str, order_id: str):
    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:560px;margin:0 auto">
      <div style="background:#16a34a;padding:20px;border-radius:8px 8px 0 0">
        <h1 style="color:#fff;margin:0">🚀 Gift is on its way!</h1>
      </div>
      <div style="background:#fff;padding:28px;border:1px solid #eee;border-top:none">
        <p style="font-size:15px;color:#333">
          The gift for <strong>{recipient_name}</strong> has been ordered and is heading your way.
        </p>
        <p style="color:#555">Walmart Order #: <strong>{order_id}</strong></p>
        <p style="color:#555">It should arrive 3 days before the birthday — already gift wrapped with a card.</p>
      </div>
    </div>"""

    _send(to_email, f"🚀 Gift shipped for {recipient_name}!", html)

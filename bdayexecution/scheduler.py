"""
Runs daily at 9am. Finds birthdays 9 days out, searches Walmart,
emails JStout for approval. Approval triggers the Playwright purchase.
"""
import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db import get_upcoming_birthdays, create_order
from walmart import search_gifts
from emailer import send_approval_email

log = logging.getLogger(__name__)


async def run_birthday_check():
    log.info("Running birthday check...")
    upcoming = get_upcoming_birthdays(days_ahead=9)
    log.info(f"Found {len(upcoming)} upcoming birthdays.")

    for r in upcoming:
        try:
            log.info(f"Searching gifts for {r['name']} ({r['gender']}, {r['gift_budget']})")
            gifts = await search_gifts(r["gender"], r["gift_budget"], r["name"])

            if not gifts:
                log.warning(f"No gifts found for {r['name']} — skipping.")
                continue

            top = gifts[0]
            order_id = create_order(
                recipient_id=r["id"],
                year=__import__("datetime").date.today().year,
                product_name=top["name"],
                product_url=top["link"],
                product_price=top["price"],
            )

            send_approval_email(order_id, r, gifts)
            log.info(f"Approval email sent for {r['name']} (order {order_id})")

        except Exception as e:
            log.error(f"Error processing {r['name']}: {e}")


def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        run_birthday_check,
        trigger="cron",
        hour=9,
        minute=0,
        id="birthday_check",
    )
    scheduler.start()
    log.info("Scheduler started — runs daily at 9:00 AM.")
    return scheduler

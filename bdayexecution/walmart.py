"""
Walmart gift search and purchase via Playwright.
Search finds top-rated, in-budget items. Purchase completes checkout.
"""
import asyncio
import os
import re
from playwright.async_api import async_playwright, TimeoutError as PWTimeout

WALMART_EMAIL    = os.getenv("WALMART_EMAIL")
WALMART_PASSWORD = os.getenv("WALMART_PASSWORD")

GENDER_KEYWORDS = {
    "Male":   ["for him", "for men", "for boys", "men's"],
    "Female": ["for her", "for women", "for girls", "women's"],
}

BUDGET_MAX = {
    "Under $25":  25,
    "$25 - $50":  50,
    "$50 - $75":  75,
    "$75 - $100": 100,
    "$100+":      150,
}


async def search_gifts(gender: str, gift_budget: str, recipient_name: str) -> list[dict]:
    """Search Walmart for top gift options. Returns up to 5 results."""
    budget = BUDGET_MAX.get(gift_budget, 50)
    query = f"best gift for {gender.lower()} under {budget} dollars"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox","--disable-dev-shm-usage"])
        ctx = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
        )
        page = await ctx.new_page()

        try:
            url = f"https://www.walmart.com/search?q={query.replace(' ', '+')}&max_price={budget}"
            await page.goto(url, timeout=20000)
            await page.wait_for_timeout(2500)

            items = await page.eval_on_selector_all(
                "[data-item-id]",
                """els => els.slice(0, 10).map(el => {
                    const name = el.querySelector('[itemprop="name"]')?.innerText?.trim() || '';
                    const priceEl = el.querySelector('[itemprop="price"]');
                    const price = priceEl ? parseFloat(priceEl.getAttribute('content') || '0') : 0;
                    const link = el.querySelector('a[href*="/ip/"]')?.href || '';
                    const rating = el.querySelector('.stars-reviews-count-node')?.innerText?.trim() || '';
                    const badge = el.querySelector('.product-badge-text')?.innerText?.trim() || '';
                    return { name, price, link, rating, badge };
                })"""
            )

            # Filter: price in budget, has a link, has a name
            filtered = [
                i for i in items
                if i["name"] and i["link"] and 5 < i["price"] <= budget
            ]

            # Sort by presence of "2-day" badge first, then by rating length (proxy for review count)
            filtered.sort(key=lambda x: (
                0 if "2-day" in x.get("badge", "").lower() else 1,
                -len(x.get("rating", ""))
            ))

            return filtered[:5]

        finally:
            await browser.close()


async def purchase_gift(product_url: str, shipping_name: str, shipping_address: str) -> str:
    """
    Log into Walmart, add item to cart, attempt gift wrap, checkout.
    Returns Walmart order ID on success.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox","--disable-dev-shm-usage"])
        ctx = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
        )
        page = await ctx.new_page()

        # ── 1. LOGIN ──
        await page.goto("https://www.walmart.com/account/login", timeout=20000)
        await page.fill('[name="email"]', WALMART_EMAIL)
        await page.fill('[name="password"]', WALMART_PASSWORD)
        await page.click('[id="sign-in-form"] button[type="submit"]')
        await page.wait_for_load_state("networkidle", timeout=15000)

        # ── 2. ADD TO CART ──
        await page.goto(product_url, timeout=20000)
        await page.wait_for_timeout(1500)

        # Try gift wrap option first
        try:
            gift_wrap = page.locator("text=Gift wrap").first
            if await gift_wrap.is_visible(timeout=3000):
                await gift_wrap.click()
        except PWTimeout:
            pass

        await page.click('[data-automation-id="atc-button"], [data-tl-id="ProductPrimaryCTA-cta_add_to_cart_button"]')
        await page.wait_for_timeout(2000)

        # ── 3. GO TO CHECKOUT ──
        await page.goto("https://www.walmart.com/checkout", timeout=20000)
        await page.wait_for_load_state("networkidle", timeout=15000)

        # ── 4. PARSE SHIPPING ADDRESS ──
        # Expected format: "Street, City, State ZIP"
        parts = [p.strip() for p in shipping_address.split(",")]
        street = parts[0] if len(parts) > 0 else ""
        city   = parts[1] if len(parts) > 1 else ""
        state_zip = parts[2].strip() if len(parts) > 2 else ""
        state_match = re.match(r"([A-Z]{2})\s+(\d{5})", state_zip)
        state = state_match.group(1) if state_match else ""
        zipcode = state_match.group(2) if state_match else ""

        # ── 5. FILL SHIPPING ──
        name_parts = shipping_name.strip().split(" ", 1)
        first = name_parts[0]
        last  = name_parts[1] if len(name_parts) > 1 else ""

        try:
            await page.fill('[name="firstName"]', first, timeout=5000)
            await page.fill('[name="lastName"]', last, timeout=5000)
            await page.fill('[name="addressLineOne"], [name="address1"]', street, timeout=5000)
            await page.fill('[name="city"]', city, timeout=5000)
            await page.select_option('[name="state"]', state, timeout=5000)
            await page.fill('[name="postalCode"], [name="zipCode"]', zipcode, timeout=5000)
            await page.click('button:has-text("Continue"), button:has-text("Save & Continue")', timeout=8000)
            await page.wait_for_timeout(2000)
        except PWTimeout:
            pass  # address may already be saved on account

        # ── 6. PLACE ORDER ──
        await page.click(
            'button:has-text("Place order"), button:has-text("Review order")',
            timeout=10000
        )
        await page.wait_for_timeout(3000)

        # ── 7. GRAB ORDER ID ──
        order_text = await page.inner_text("body")
        match = re.search(r"[Oo]rder\s*#?\s*(\d{7,})", order_text)
        order_id = match.group(1) if match else "UNKNOWN"

        await browser.close()
        return order_id

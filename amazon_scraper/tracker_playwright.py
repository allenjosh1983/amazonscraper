import json
import asyncio
import os
from playwright.async_api import async_playwright
from emailer import send_email
from config import PRODUCT_URL, TARGET_PRICE

PROFILE_DIR = "amazon_price_tracker/playwright_profile"

def load_products(path="products.json"):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # Fallback to .env config
        return [{
            "name": "Amazon Product",
            "url": PRODUCT_URL,
            "target_price": TARGET_PRICE
        }]

async def get_price_amazon(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(PROFILE_DIR, headless=False)
        page = await browser.new_page()

        try:
            print(f"Navigating to: {url}")
            await page.goto(url, timeout=60000)
            await page.wait_for_timeout(3000)

            # ✅ Try Add to Cart
            try:
                await page.click("#add-to-cart-button", timeout=5000)
                print("🛒 Added to cart (direct)")
            except:
                print("⚠️ Add to Cart not found. Trying Buying Options...")
                try:
                    await page.click("text=See All Buying Options", timeout=5000)
                    await page.wait_for_selector("input[name='submit.addToCart']", timeout=5000)
                    await page.click("input[name='submit.addToCart']")
                    print("🛒 Added to cart (via Buying Options)")
                except Exception as e:
                    print(f"❌ Buying Options failed: {e}")
                    await page.screenshot(path="amazon_price_tracker/buying_options_fail.png")
                    return None

            await page.wait_for_timeout(3000)
            await page.goto("https://www.amazon.com/gp/cart/view.html")
            await page.wait_for_timeout(3000)

            # ✅ Extract price
            try:
                price_element = await page.wait_for_selector("span:has-text('$')", timeout=5000)
                price_text = await price_element.inner_text()
                price = float(price_text.replace("$", "").replace(",", "").strip())
                print(f"✅ Found cart price: ${price}")
            except:
                print("❌ Could not find price in cart")
                price = None

            # ✅ Save debug artifacts
            await page.screenshot(path="amazon_price_tracker/amazon_screenshot.png")
            html = await page.content()
            with open("amazon_price_tracker/amazon_debug.html", "w", encoding="utf-8") as f:
                f.write(html)

        except Exception as e:
            print(f"❌ Playwright failed: {e}")
            price = None

        await browser.close()
        return price

async def check_prices():
    products = load_products()

    for product in products:
        print(f"\n🔍 Checking: {product['name']}")
        current_price = await get_price_amazon(product["url"])

        if current_price is None:
            print(f"❌ Could not fetch price for {product['url']}")
            continue

        print(f"Current price: ${current_price} | Target: ${product['target_price']}")
        if current_price <= product["target_price"]:
            send_email(product["name"], product["url"], current_price)

if __name__ == "__main__":
    asyncio.run(check_prices())
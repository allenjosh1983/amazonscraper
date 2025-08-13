import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from emailer import send_email  # ✅ Correct import

def get_price_amazon(url):
    options = uc.ChromeOptions()
    options.add_argument("--user-data-dir=C:\\Users\\5540\\AmazonScraperProfile")
    driver = uc.Chrome(options=options)

    price = None

    try:
        driver.get(url)
        time.sleep(3)

        wait = WebDriverWait(driver, 10)

        # ✅ Try Add to Cart directly
        try:
            add_btn = wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-button")))
            add_btn.click()
            print("🛒 Added to cart (direct)")
        except:
            print("⚠️ Add to Cart not found. Trying Buying Options...")

            # ✅ Fallback: Click "See All Buying Options" by visible text
            try:
                buying_options_btn = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//a[contains(text(), 'See All Buying Options')]")
                ))
                buying_options_btn.click()
                print("🔄 Navigated to Buying Options")
                time.sleep(3)

                # ✅ Try Add to Cart again on buying options page
                try:
                    alt_add_btn = wait.until(EC.element_to_be_clickable((By.NAME, "submit.addToCart")))
                    alt_add_btn.click()
                    print("🛒 Added to cart (via Buying Options)")
                except:
                    print("❌ Could not click Add to Cart in Buying Options")
                    return None

            except:
                print("❌ Could not click See All Buying Options")
                return None

        time.sleep(3)

        # ✅ Navigate to cart
        driver.get("https://www.amazon.com/gp/cart/view.html")
        time.sleep(3)

        # ✅ Flexible XPath for cart price
        try:
            cart_price = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//span[contains(text(), '$')]")
            ))
            price_text = cart_price.text.strip().replace("$", "").replace(",", "")
            price = float(price_text)
            print(f"✅ Found cart price: ${price}")
        except:
            print("❌ Could not find price in cart")

    except Exception as e:
        print(f"❌ Selenium failed: {e}")

    finally:
        # ✅ Always save debug artifacts
        try:
            with open("amazon_debug.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            driver.save_screenshot("amazon_screenshot.png")
        except:
            print("⚠️ Failed to save debug artifacts")

        try:
            driver.quit()
        except:
            pass  # Suppress WinError 6

    return price

def check_prices():
    # ✅ Baked-in test product
    product = {
        "name": "Echo Dot",
        "url": "https://www.amazon.com/dp/B07FZ8S74R",
        "target_price": 999.99
    }

    current_price = get_price_amazon(product["url"])

    if current_price is None:
        print(f"Could not fetch price for {product['url']}")
        return

    print(f"Current price: ${current_price} | Target: ${product['target_price']}")
    if current_price <= product["target_price"]:
        send_email(product["name"], product["url"], current_price)

if __name__ == "__main__":
    check_prices()
import os
import json
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

PRODUCT_URL = os.getenv("PRODUCT_URL")
TARGET_PRICE = float(os.getenv("TARGET_PRICE", "0"))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_FILE = os.path.join(BASE_DIR, "products.json")

def load_products():
    if not os.path.exists(PRODUCTS_FILE):
        return []  # Return empty list if file doesn't exist
    with open(PRODUCTS_FILE, "r") as f:
        return json.load(f)

def save_products(products):
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(products, f, indent=2)

if __name__ == "__main__":
    products = load_products()
    print(f"Loaded {len(products)} products.")
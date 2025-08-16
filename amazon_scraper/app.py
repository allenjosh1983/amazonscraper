from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import asyncio
import json
import os

from tracker_playwright import get_price_amazon
from emailer import send_email
from config import load_products, save_products

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Needed for Flask-WTF forms and flash messages

@app.route("/", methods=["GET", "POST"])
def index():
    products = load_products()

    if request.method == "POST":
        selected_name = request.form.get("product") or request.form.get("name")
        url = request.form.get("url")
        target_price = request.form.get("target_price")

        if not url or not target_price:
            flash("URL and target price are required.", "error")
            return redirect("/")

        try:
            target = float(target_price)
        except ValueError:
            flash("Target price must be a number.", "error")
            return redirect("/")

        async def check():
            current_price = await get_price_amazon(url)
            if current_price is None:
                flash("Could not fetch price.", "error")
            else:
                msg = f"Current price: ${current_price:.2f}"
                if current_price <= target:
                    send_email(selected_name, url, current_price)
                    msg += " ✅ Alert sent!"
                flash(msg, "info")

        asyncio.run(check())
        return redirect("/")

    return render_template("index.html", products=products)

@app.route("/delete/<int:index>", methods=["POST"])
def delete_product(index):
    products = load_products()
    try:
        removed = products.pop(index)
        save_products(products)
        flash(f"Deleted {removed['name']}", "success")
    except IndexError:
        flash("Invalid product index", "error")
    return redirect("/")

@app.route("/edit/<int:index>", methods=["POST"])
def edit_product(index):
    products = load_products()
    if index < 0 or index >= len(products):
        flash("Invalid product index", "error")
        return redirect("/")

    name = request.form.get("name")
    url = request.form.get("url")
    target_price = request.form.get("target_price")

    if not name or not url or not target_price:
        flash("All fields are required for editing", "error")
        return redirect("/")

    try:
        target_price = float(target_price)
        products[index] = {
            "name": name,
            "url": url,
            "target_price": target_price
        }
        save_products(products)
        flash(f"Updated {name}", "success")
    except ValueError:
        flash("Target price must be a number", "error")

    return redirect("/")
@app.route("/health")
def health_check():
    try:
        from flask_wtf import FlaskForm
        from wtforms import StringField
        from dotenv import load_dotenv
        import os
        import json

        load_dotenv()
        email = os.getenv("EMAIL_ADDRESS")
        assert email, "EMAIL_ADDRESS not set"

        with open("products.json", "r") as f:
            products = json.load(f)
        assert isinstance(products, list), "products.json is not a list"

        return "✅ All systems go", 200
    except Exception as e:
        return f"❌ Health check failed: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
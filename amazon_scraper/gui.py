import tkinter as tk
from tkinter import ttk, messagebox
import asyncio
from tracker_playwright import get_price_amazon
from emailer import send_email
from config import tracked_products  # Dictionary: {name: url}

def autofill_url(event=None):
    product_name = selected_product.get()
    url = tracked_products.get(product_name, "")
    url_entry.delete(0, tk.END)
    url_entry.insert(0, url)

def run_check():
    url = url_entry.get()
    try:
        target = float(price_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Target price must be a number.")
        return

    async def check():
        current_price = await get_price_amazon(url)
        if current_price is None:
            messagebox.showerror("Error", "Could not fetch price.")
        else:
            msg = f"Current price: ${current_price:.2f}"
            if current_price <= target:
                send_email("Amazon Product", url, current_price)
                msg += "\n\n✅ Alert sent!"
            messagebox.showinfo("Price Check", msg)

    asyncio.run(check())

# GUI layout
root = tk.Tk()
root.title("Amazon Price Tracker")

# Product dropdown
tk.Label(root, text="Select Product:").grid(row=0, column=0, sticky="e")
selected_product = tk.StringVar()
product_dropdown = ttk.Combobox(root, textvariable=selected_product, width=47)
product_dropdown['values'] = list(tracked_products.keys())
product_dropdown.grid(row=0, column=1)
product_dropdown.bind("<<ComboboxSelected>>", autofill_url)

# URL entry
tk.Label(root, text="Product URL:").grid(row=1, column=0, sticky="e")
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=1, column=1)

# Target price entry
tk.Label(root, text="Target Price:").grid(row=2, column=0, sticky="e")
price_entry = tk.Entry(root, width=20)
price_entry.grid(row=2, column=1, sticky="w")

# Check button
check_button = tk.Button(root, text="Check Price", command=run_check)
check_button.grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()
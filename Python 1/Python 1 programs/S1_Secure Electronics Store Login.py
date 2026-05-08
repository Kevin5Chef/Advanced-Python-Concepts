import tkinter as tk
from tkinter import messagebox
from functools import wraps
print("SY-5, Kevin Victor, Roll No.-30")
# ---------------- AUTHORIZED USERS ----------------
USERS = {
    "kevin": "1234",
    "admin": "admin123",
    "alex": "pass123",
    "maria": "secure456",
    "john": "qwerty"
}

current_user = None
cart = []

# ---------------- DECORATOR ----------------
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user is None:
            messagebox.showerror("Access Denied", "Please login first.")
            return
        return func(*args, **kwargs)
    return wrapper


# ---------------- PRODUCT DATA ----------------
PRODUCTS = [
    {"name": "Gaming Laptop", "price": 82000, "desc": "RTX GPU, i7 CPU, 16GB RAM"},
    {"name": "Smartphone", "price": 42000, "desc": "OLED Display, 5G Support"},
    {"name": "Wireless Earbuds", "price": 3200, "desc": "Noise Cancellation"},
    {"name": "AirPods Pro", "price": 19999, "desc": "Premium ANC Earbuds"},
    {"name": "Bluetooth Headphones", "price": 5400, "desc": "Deep Bass Audio"},
    {"name": "Cooling Pad", "price": 1800, "desc": "Laptop Cooling Support"},
    {"name": "Gaming PC", "price": 115000, "desc": "RTX 4070, Ryzen 7"},
    {"name": "Fast Charger", "price": 1500, "desc": "65W USB-C Charger"},
    {"name": "Power Bank", "price": 2200, "desc": "20000mAh Battery"},
    {"name": "Smart Watch", "price": 8500, "desc": "Heart Rate + GPS"},
    {"name": "Fitness Band", "price": 4500, "desc": "Workout Tracking"},
    {"name": "Arduino Starter Kit", "price": 5200, "desc": "IoT Learning Kit"},
    {"name": "Raspberry Pi Kit", "price": 6800, "desc": "Mini Computer Kit"},
    {"name": "USB Hub", "price": 1200, "desc": "Multi-port Expansion"},
    {"name": "Mechanical Keyboard", "price": 7400, "desc": "RGB Backlit Keys"}
]


# ---------------- LOGIN ----------------
def login():
    global current_user
    username = username_entry.get()
    password = password_entry.get()

    if username in USERS and USERS[username] == password:
        current_user = username
        messagebox.showinfo("Login Success", f"Welcome {username}!")
        open_store()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")


# ---------------- LOGOUT ----------------
def logout(store_window):
    global current_user, cart
    current_user = None
    cart.clear()
    messagebox.showinfo("Logged Out", "You have been logged out safely.")
    store_window.destroy()


# ---------------- STORE WINDOW ----------------
@login_required
def open_store():
    store_window = tk.Toplevel(root)
    store_window.title("Electronics Store")
    store_window.geometry("720x470")

    header = tk.Frame(store_window)
    header.pack(fill="x", pady=5)

    tk.Label(header, text="Available Products", font=("Arial", 16, "bold")).pack(side="left", padx=10)
    tk.Button(header, text="Log Out", fg="red",
              command=lambda: logout(store_window)).pack(side="right", padx=10)

    listbox = tk.Listbox(store_window, width=85, height=14)
    listbox.pack(pady=10)

    for p in PRODUCTS:
        listbox.insert(tk.END, f"{p['name']} — ₹{p['price']}")

    def view_details():
        try:
            selected = listbox.curselection()[0]
            product = PRODUCTS[selected]
            show_product_details(product)
        except:
            messagebox.showwarning("Selection Error", "Please select a product.")

    def add_to_cart():
        try:
            selected = listbox.curselection()[0]
            cart.append(PRODUCTS[selected])
            messagebox.showinfo("Added to Cart", "Product added successfully!")
        except:
            messagebox.showwarning("Selection Error", "Select a product first.")

    btn_frame = tk.Frame(store_window)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="View Details", command=view_details).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Add to Cart", command=add_to_cart).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="View Cart", command=open_cart).grid(row=0, column=2, padx=5)


# ---------------- PRODUCT DETAILS ----------------
def show_product_details(product):
    details_window = tk.Toplevel(root)
    details_window.title(product["name"])
    details_window.geometry("420x260")

    tk.Label(details_window, text=product["name"], font=("Arial", 14, "bold")).pack(pady=5)
    tk.Label(details_window, text=f"Price: ₹{product['price']}").pack(pady=5)
    tk.Label(details_window, text=f"Description:\n{product['desc']}", wraplength=360).pack(pady=5)

    tk.Button(details_window, text="Add to Cart",
              command=lambda: cart.append(product)).pack(pady=10)


# ---------------- CART WINDOW ----------------
@login_required
def open_cart():
    cart_window = tk.Toplevel(root)
    cart_window.title("Your Cart")
    cart_window.geometry("460x360")

    tk.Label(cart_window, text="Shopping Cart", font=("Arial", 16, "bold")).pack(pady=5)

    listbox = tk.Listbox(cart_window, width=65, height=12)
    listbox.pack(pady=5)

    total = 0
    for item in cart:
        listbox.insert(tk.END, f"{item['name']} — ₹{item['price']}")
        total += item["price"]

    tk.Label(cart_window, text=f"Total: ₹{total}", font=("Arial", 12, "bold")).pack(pady=5)

    def checkout():
        if not cart:
            messagebox.showwarning("Empty Cart", "Add products first.")
            return
        messagebox.showinfo("Payment Success", "Payment completed successfully!")
        cart.clear()
        cart_window.destroy()

    tk.Button(cart_window, text="Proceed to Payment", command=checkout).pack(pady=10)


# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Secure Electronics Store Login")
root.geometry("400x260")

tk.Label(root, text="Login System", font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(root, text="Username").pack()
username_entry = tk.Entry(root)
username_entry.pack()

tk.Label(root, text="Password").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

tk.Button(root, text="Login", command=login).pack(pady=10)

root.mainloop()

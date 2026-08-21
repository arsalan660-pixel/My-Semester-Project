from tkinter import *
import state
from product import get_products


def on_enter_green(e): e.widget["bg"] = "#008b87"
def on_leave_green(e): e.widget["bg"] = "#00a49f"
def on_enter_blue(e): e.widget["bg"] = "#245de6"
def on_leave_blue(e): e.widget["bg"] = "#3a77ff"
def on_enter_red(e): e.widget["bg"] = "#e63939"
def on_leave_red(e): e.widget["bg"] = "#ff4d4d"


def open_dashboard(window, user):

    dashboard = Toplevel(window)
    dashboard.title("Dashboard")
    dashboard.geometry("600x500")
    dashboard.configure(bg="#dff6f0")

    user_name = user[1]
    user_email = user[2]

    welcome_label = Label(dashboard,text=f"Welcome, {user_name}",font=("Helvetica", 24, "bold"),bg="#dff6f0",fg="#002f34")
    welcome_label.pack(pady=(25,5))

    email_label = Label(dashboard,text=f"Email: {user_email}",font=("Helvetica", 11),bg="#dff6f0",fg="gray")
    email_label.pack(pady=(0,30))

    # Stats Row
    all_products = get_products()
    my_products = [p for p in all_products if p.seller == user[1]]
    active_count = len([p for p in my_products if p.status != "sold"])
    sold_count = len([p for p in my_products if p.status == "sold"])
    total_value = sum(float(p.price) for p in my_products)
    stats_frame = Frame(dashboard, bg="#dff6f0")
    stats_frame.pack(pady=(0, 20))
    Label(stats_frame, text=f"{active_count} Active", font=("Helvetica", 11, "bold"), bg="#dff6f0", fg="#00a49f").pack(side=LEFT, padx=10)
    Label(stats_frame, text=f"{sold_count} Sold", font=("Helvetica", 11, "bold"), bg="#dff6f0", fg="#7f8c8d").pack(side=LEFT, padx=10)
    Label(stats_frame, text=f"Rs. {total_value:,.0f} Total", font=("Helvetica", 11, "bold"), bg="#dff6f0", fg="#002f34").pack(side=LEFT, padx=10)

    my_listings_btn = Label(dashboard, text="My Listings", bg="#8b5cf6", fg="white", font=("Helvetica", 14, "bold"), width=22, height=2, cursor="hand2")
    my_listings_btn.pack(pady=(0, 15))
    my_listings_btn.bind("<Button-1>", lambda e: open_my_listings(window, user))

    # SELL PRODUCT BUTTON
    dashboard_sell_btn = Label(dashboard,text="Sell Product",bg="#00a49f",fg="white",font=("Helvetica", 14, "bold"),width=22,height=2,cursor="hand2")
    dashboard_sell_btn.pack(pady=(0,15))

    def go_to_sell():
        from product_windows import open_add_product
        open_add_product(window, user)

    dashboard_sell_btn.bind("<Button-1>", lambda e: go_to_sell())
    dashboard_sell_btn.bind("<Enter>", on_enter_green)
    dashboard_sell_btn.bind("<Leave>", on_leave_green)

    # VIEW PRODUCTS BUTTON
    def go_to_products():
        dashboard.withdraw()
        from product_windows import open_products_window
        open_products_window(window, dashboard)

    dashboard_view_btn = Label(dashboard,text=" View Products",bg="#3a77ff",fg="white",font=("Helvetica", 14, "bold"),width=22,height=2,cursor="hand2" )
    dashboard_view_btn.pack(pady=(0,15))
    dashboard_view_btn.bind("<Button-1>", lambda e: go_to_products())

    # LOGOUT BUTTON
    dashboard_logout_btn = Label(dashboard,text="Logout",bg="#ff4d4d",fg="white",font=("Helvetica", 14, "bold"),width=22,height=2,cursor="hand2")
    dashboard_logout_btn.pack(pady=(15,10))
    dashboard_logout_btn.bind("<Button-1>",lambda e: dashboard.destroy())
    dashboard_logout_btn.bind("<Enter>", on_enter_red)
    dashboard_logout_btn.bind("<Leave>", on_leave_red)


def open_my_listings(window, user):
    listings_window = Toplevel(window)
    listings_window.title("My Listings")
    listings_window.geometry("900x700")
    listings_window.configure(bg="#dff6f0")

    Label(listings_window, text="My Listings", font=("Helvetica", 24, "bold"), bg="#dff6f0", fg="#002f34").pack(pady=20)

    canvas = Canvas(listings_window, bg="#dff6f0", highlightthickness=0)
    scrollbar = Scrollbar(listings_window, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#dff6f0")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    products = get_products()
    my_products = [p for p in products if p.seller == user[1]]

    row = 0
    col = 0
    for product in my_products:
        product_id = product.id
        title = product.title
        price = product.price
        status = product.status

        card = Frame(scrollable_frame, bg="white", width=280, height=200, highlightbackground="#e0e0e0", highlightthickness=1)
        card.grid(row=row, column=col, padx=15, pady=15)
        card.grid_propagate(False)

        Label(card, text=title, font=("Helvetica", 14, "bold"), bg="white", fg="#002f34").pack(anchor="w", padx=15, pady=(15, 5))
        Label(card, text=f"Rs. {price}", font=("Helvetica", 12, "bold"), bg="white", fg="#002f34").pack(anchor="w", padx=15)
        status_color = "#e63939" if status == "sold" else "#00a49f"
        Label(card, text=status.upper(), font=("Helvetica", 10, "bold"), bg="white", fg=status_color).pack(anchor="w", padx=15, pady=10)

        col += 1
        if col == 3:
            col = 0
            row += 1
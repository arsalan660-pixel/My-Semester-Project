from tkinter import *
import state
from product import get_products


def on_enter_hover(e):
    e.widget["bg"] = e.widget.hover_color


def on_leave_hover(e):
    e.widget["bg"] = e.widget.base_color


def make_action_button(parent, text, base_color, hover_color, command):
    btn = Button(parent, text=text, bg=base_color, fg="white",
                 activebackground=hover_color, activeforeground="white",
                 font=("Helvetica", 12, "bold"), relief="flat", bd=0,
                 cursor="hand2", anchor="w", padx=18, pady=12, command=command)
    btn.base_color = base_color
    btn.hover_color = hover_color
    btn.bind("<Enter>", on_enter_hover)
    btn.bind("<Leave>", on_leave_hover)
    return btn


def open_dashboard(window, user):

    dashboard = Toplevel(window)
    dashboard.title("Dashboard")
    dashboard.geometry("420x560")
    dashboard.configure(bg="#dff6f0")

    user_name = user[1]
    user_email = user[2]

    header = Frame(dashboard, bg="#dff6f0")
    header.pack(fill="x", padx=25, pady=(25, 15))

    initials = "".join([w[0].upper() for w in user_name.split()][:2]) or "U"
    avatar = Label(header, text=initials, bg="#002f34", fg="white",
                    font=("Helvetica", 16, "bold"), width=3, height=1)
    avatar.pack(side=LEFT, padx=(0, 12))

    name_block = Frame(header, bg="#dff6f0")
    name_block.pack(side=LEFT)
    Label(name_block, text=user_name, font=("Helvetica", 16, "bold"),
          bg="#dff6f0", fg="#002f34").pack(anchor="w")
    Label(name_block, text=user_email, font=("Helvetica", 10),
          bg="#dff6f0", fg="gray").pack(anchor="w")

    # Stats as metric cards instead of a plain text row
    all_products = get_products()
    my_products = [p for p in all_products if p.seller == user[1]]
    active_count = len([p for p in my_products if p.status != "sold"])
    sold_count = len([p for p in my_products if p.status == "sold"])
    
    # Safe calculation taake app crash na ho
    total_value = 0
    for p in my_products:
        try:
            total_value += float(p.price)
        except ValueError:
            pass

    stats_frame = Frame(dashboard, bg="#dff6f0")
    stats_frame.pack(fill="x", padx=25, pady=(0, 20))

    def metric_card(parent, label, value, value_color):
        card = Frame(parent, bg="white", highlightthickness=1,
                     highlightbackground="#e0e0e0")
        Label(card, text=str(value), font=("Helvetica", 15, "bold"),
              bg="white", fg=value_color).pack(pady=(10, 0))
        Label(card, text=label, font=("Helvetica", 9),
              bg="white", fg="#7f8c8d").pack(pady=(0, 10))
        return card

    metric_card(stats_frame, "Active", active_count, "#00a49f").pack(side=LEFT, fill="both", expand=True, padx=(0, 6))
    metric_card(stats_frame, "Sold", sold_count, "#7f8c8d").pack(side=LEFT, fill="both", expand=True, padx=6)
    metric_card(stats_frame, "Total value", f"Rs. {total_value:,.0f}", "#002f34").pack(side=LEFT, fill="both", expand=True, padx=(6, 0))

    # Action buttons - compact, icon-led, consistent height, grouped in one card
    actions_frame = Frame(dashboard, bg="#dff6f0")
    actions_frame.pack(fill="x", padx=25, pady=(5, 0))

    make_action_button(actions_frame, "\U0001F4CB  My Listings", "#8b5cf6", "#7c4fe0",
                        lambda: open_my_listings(window, user)).pack(fill="x", pady=(0, 8))

    def go_to_sell():
        from product_windows import open_add_product
        open_add_product(window, user)

    make_action_button(actions_frame, "\U0001F4B0  Sell Product", "#00a49f", "#008b87",
                        go_to_sell).pack(fill="x", pady=(0, 8))

    def go_to_products():
        dashboard.withdraw()
        from product_windows import open_products_window
        open_products_window(window, dashboard)

    make_action_button(actions_frame, "\U0001F4E6  View Products", "#3a77ff", "#245de6",
                        go_to_products).pack(fill="x", pady=(0, 8))

    Frame(dashboard, bg="#dff6f0", height=15).pack()

    make_action_button(actions_frame, "\U0001F6AA  Logout", "#ff4d4d", "#e63939",
                        dashboard.destroy).pack(fill="x", pady=(10, 0))


def open_my_listings(window, user):
    listings_window = Toplevel(window)
    listings_window.title("My Listings")
    listings_window.geometry("900x700")
    listings_window.configure(bg="#dff6f0")

    Label(listings_window, text="My Listings", font=("Helvetica", 24, "bold"), bg="#dff6f0", fg="#002f34").pack(pady=20)

    # Main Card Wrapper for the whole list
    card = Frame(listings_window, bg="white", highlightthickness=1, highlightbackground="#e0e0e0", bd=0)
    card.pack(padx=30, pady=(0, 30), fill="both", expand=True)

    inner = Frame(card, bg="white")
    inner.pack(padx=15, pady=15, fill="both", expand=True)

    # Canvas and Scrollbar set to white background to match inner frame
    canvas = Canvas(inner, bg="white", highlightthickness=0)
    scrollbar = Scrollbar(inner, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="white")

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
        title = product.title
        price = product.price
        status = product.status

        # Individual item card (slightly distinct from white background)
        item_card = Frame(scrollable_frame, bg="#f8f9fa", width=250, height=180, highlightbackground="#e0e0e0", highlightthickness=1)
        item_card.grid(row=row, column=col, padx=12, pady=12)
        item_card.grid_propagate(False)

        Label(item_card, text=title, font=("Helvetica", 14, "bold"), bg="#f8f9fa", fg="#002f34").pack(anchor="w", padx=15, pady=(15, 5))
        Label(item_card, text=f"Rs. {price}", font=("Helvetica", 12, "bold"), bg="#f8f9fa", fg="#002f34").pack(anchor="w", padx=15)
        
        status_color = "#ff4d4d" if status == "sold" else "#00a49f"
        Label(item_card, text=status.upper(), font=("Helvetica", 10, "bold"), bg="#f8f9fa", fg=status_color).pack(anchor="w", padx=15, pady=10)

        col += 1
        if col == 3:
            col = 0
            row += 1
# =========================
# IMPORTS
# =========================

from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from auth import register_user, login_user, delete_user
from product import add_product, get_products,delete_product,mark_as_sold
import os
from collections import deque
recently_viewed={}


current_user = None

# =========================
# MAIN WINDOW
# =========================

window = Tk()
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)

window.title("OLX Desktop Clone")
window.geometry("900x650")
window.configure(bg="#dff6f0")

window.resizable(False, False)
navbar=Frame(window,bg="#002f34",height=60)
navbar.pack(fill="x",side="top")
def navbar_enter(e):
    e.widget.config(bg="#004d52")

def navbar_leave(e):
    e.widget.config(bg="#002f34")
home_btn=Label(navbar,text="🏠 Home",bg="#002f34",fg="white",font=("Helvetica",12,"bold"),cursor="hand2")
home_btn.pack(side="left",padx="15")
home_btn.bind("<Enter>", navbar_enter)
home_btn.bind("<Leave>", navbar_leave)
sell_btn=Label(navbar,text="➕ Sell",bg="#002f34",fg="white",font=("Helvetica",12,"bold"),cursor="hand2")
sell_btn.pack(side="left",padx="15")
products_btn=Label(navbar,text="📦 Products",bg="#002f34",fg="white",font=("Helvetica",12,"bold"),cursor="hand2")
products_btn.pack(side="left",padx="15")
products_btn.bind("<Enter>", navbar_enter)
products_btn.bind("<Leave>", navbar_leave)
logout_btn=Label(navbar,text="🚪 Logout",bg="#002f34",fg="white",font=("Helvetica",12,"bold"),cursor="hand2")
logout_btn.pack(side="left",padx="15")
logout_btn.bind("<Enter>", navbar_enter)
logout_btn.bind("<Leave>", navbar_leave)
def open_home():
    for widget in window.winfo_children():
        if isinstance(widget, Toplevel):
            widget.destroy()
    main_frame.pack(fill="both",expand=True)
    
def open_sell():
    if current_user:

        open_add_product(current_user)

    else:

        messagebox.showerror(
            "Login Required",
            "Please login first"
        )  
def open_products():
    open_products_window()
def logout():
    global current_user

    current_user = None
    for widget in window.winfo_children():
        if isinstance(widget, Toplevel):
            widget.destroy()

    messagebox.showinfo(
        "Logout",
        "Logged out successfully"
    )

def track_view(product,user) :
    if user[2] not in recently_viewed :
        recently_viewed[user[2]]=deque(maxlen=5)
    recently_viewed[user[2]].append(product)


# =========================
# MAIN FRAME
# =========================

main_frame = Frame(window, bg="#dff6f0")
main_frame.pack(expand=True)

# =========================
# LOGO
# =========================

current_folder = os.path.dirname(__file__)

logo_path = os.path.join(current_folder, "logo.png")

logo = PhotoImage(file=logo_path)

logo = logo.subsample(15, 15)

logo_label = Label(
    main_frame,
    image=logo,
    bg="#dff6f0"
)

logo_label.pack(pady=20)

# =========================
# TITLE
# =========================

title = Label(
    main_frame,
    text="Buy & Sell Anything Easily",
    font=("Helvetica", 30, "bold"),
    bg="#dff6f0",
    fg="#002f34"
)

title.pack(pady=10)

subtitle = Label(
    main_frame,
    text="Pakistan's Modern Desktop Marketplace",
    font=("Helvetica", 12),
    bg="#dff6f0",
    fg="gray"
)

subtitle.pack(pady=(0, 30))

# =========================
# HOVER EFFECTS
# =========================

def on_enter_green(e):
    e.widget["bg"] = "#008b87"

def on_leave_green(e):
    e.widget["bg"] = "#00a49f"

def on_enter_blue(e):
    e.widget["bg"] = "#245de6"

def on_leave_blue(e):
    e.widget["bg"] = "#3a77ff"

def on_enter_red(e):
    e.widget["bg"] = "#e63939"

def on_leave_red(e):
    e.widget["bg"] = "#ff4d4d"

# =========================
# DASHBOARD
# =========================
def open_dashboard(user):

    dashboard = Toplevel(window)

    dashboard.title("Dashboard")

    dashboard.geometry("600x500")

    dashboard.configure(bg="#dff6f0")

    user_name = user[1]
    user_email = user[2]

    welcome_label = Label(
        dashboard,
        text=f"Welcome, {user_name}",
        font=("Helvetica", 24, "bold"),
        bg="#dff6f0",
        fg="#002f34"
    )

    welcome_label.pack(pady=25)

    email_label = Label(
        dashboard,
        text=f"Email: {user_email}",
        font=("Helvetica", 11),
        bg="#dff6f0",
        fg="gray"
    )

    email_label.pack(pady=10)

    # SELL PRODUCT BUTTON

    dashboard_sell_btn = Label(
        dashboard,
        text="Sell Product",
        bg="#00a49f",
        fg="white",
        font=("Helvetica", 14, "bold"),
        width=22,
        height=2,
        cursor="hand2"
    )

    dashboard_sell_btn.pack(pady=15)

    dashboard_sell_btn.bind(
        "<Button-1>",
        lambda e: open_add_product(user)
    )

    dashboard_sell_btn.bind("<Enter>", on_enter_green)
    dashboard_sell_btn.bind("<Leave>", on_leave_green)

    # VIEW PRODUCTS BUTTON

    dashboard_view_btn = Label(
        dashboard,
        text=" View Products",
        bg="#3a77ff",
        fg="white",
        font=("Helvetica", 14, "bold"),
        width=22,
        height=2,
        cursor="hand2"
    )

    dashboard_view_btn.pack(pady=15)

    dashboard_view_btn.bind(
        "<Button-1>",
        lambda e: open_products_window()
    )

    dashboard_view_btn.bind("<Enter>", on_enter_blue)
    dashboard_view_btn.bind("<Leave>", on_leave_blue)

    # LOGOUT BUTTON

    dashboard_logout_btn = Label(
        dashboard,
        text="Logout",
        bg="#ff4d4d",
        fg="white",
        font=("Helvetica", 14, "bold"),
        width=22,
        height=2,
        cursor="hand2"
    )

    dashboard_logout_btn.pack(pady=30)

    dashboard_logout_btn.bind(
        "<Button-1>",
        lambda e: dashboard.destroy()
    )

    dashboard_logout_btn.bind("<Enter>", on_enter_red)
    dashboard_logout_btn.bind("<Leave>", on_leave_red)
    
# =========================
# ADD PRODUCT WINDOW
# =========================

def open_add_product(user):
    

    add_window = Toplevel(window)

    add_window.title("Sell Product")

    add_window.geometry("500x650")

    add_window.configure(bg="#dff6f0")
    add_window.grab_set()

    seller_name = user[1]

    heading = Label(
        add_window,
        text="Sell Your Product",
        font=("Helvetica", 22, "bold"),
        bg="#dff6f0",
        fg="#002f34"
    )

    heading.pack(pady=20)

    # PRODUCT TITLE

    Label(
        add_window,
        text="Product Title",
        font=("Helvetica", 12, "bold"),
        bg="#dff6f0"
    ).pack()

    title_entry = Entry(
        add_window,
        width=35,
        font=("Helvetica", 11)
    )

    title_entry.pack(pady=8)

    # PRICE

    Label(
        add_window,
        text="Price",
        font=("Helvetica", 12, "bold"),
        bg="#dff6f0"
    ).pack()

    price_entry = Entry(
        add_window,
        width=35,
        font=("Helvetica", 11)
    )

    price_entry.pack(pady=8)

    #category
    Label(add_window,
          text="Category",
          font=("Helvetica",12,"bold"),
          bg="#dff6f0").pack()
    category_var=StringVar()
    category_var.set("Electronics")

    category_menu=OptionMenu(add_window,category_var,"Electronics","Fashion","Furniture","Automobiles","Books","other")
    category_menu.config(width=20,font=("helvetica",11))
    category_menu.pack(pady=8)
                             

    # DESCRIPTION

    Label(
        add_window,
        text="Description",
        font=("Helvetica", 12, "bold"),
        bg="#dff6f0"
    ).pack()

    desc_text = Text(
        add_window,
        width=35,
        height=6,
        font=("Helvetica", 11)
    )

    desc_text.pack(pady=8)

    # IMAGE UPLOAD

    image_path = StringVar()

    def upload_image():

        file = filedialog.askopenfilename(
            parent=add_window,
            title="Select Product Image",
            filetypes=[
                ("PNG Files", "*.png"),
                ("JPG Files", "*.jpg"),
                ("JPEG Files", "*.jpeg")
            ]
        )

        if file:
            image_path.set(file)
            image_label.config(text="✅ Image Selected")

    upload_btn = Label(
        add_window,
        text="📷 Upload Image",
        bg="#3a77ff",
        fg="white",
        font=("Helvetica", 12, "bold"),
        width=20,
        height=2,
        cursor="hand2"
    )

    upload_btn.pack(pady=15)

    upload_btn.bind(
        "<Button-1>",
        lambda e: upload_image()
    )

    image_label = Label(
        add_window,
        text="No Image Selected",
        font=("Helvetica", 10),
        bg="#dff6f0",
        fg="gray"
    )

    image_label.pack()

    # SAVE PRODUCT

    def save_product():

        title = title_entry.get()

        price = price_entry.get()

        description = desc_text.get("1.0", END)
        category=category_var.get()

        if title == "" or price == "" or description.strip() == "":

            messagebox.showerror(
                "Error",
                "Please fill all fields"
            )

            return

        add_product(
            title,
            price,
            description,
            seller_name,
            image_path.get(),
            category
        )

        messagebox.showinfo(
            "Success",
            "Product Added Successfully"
        )

        add_window.destroy()

    # SAVE BUTTON

    save_btn = Label(
        add_window,
        text="💰 Sell Product",
        bg="#00a49f",
        fg="white",
        font=("Helvetica", 13, "bold"),
        width=22,
        height=2,
        cursor="hand2"
    )

    save_btn.pack(pady=25)

    save_btn.bind(
        "<Button-1>",
        lambda e: save_product()
    )

# =========================
# VIEW PRODUCTS WINDOW
# =========================

def open_products_window():
    selected_category = "ALL"

    products_window = Toplevel(window)

    products_window.title("All Products")

    products_window.geometry("1300x800")

    products_window.minsize(1200,750)

    products_window.configure(bg="#dff6f0")

    # =========================
    # HEADING
    # =========================

    heading = Label(
        products_window,
        text="Available Products",
        font=("Helvetica", 28, "bold"),
        bg="#dff6f0",
        fg="#002f34"
    )

    heading.pack(pady=20)

    # =========================
    # TOP BAR
    # =========================

    top_frame = Frame(
        products_window,
        bg="#dff6f0"
    )

    top_frame.pack(fill="x", padx=20)

    back_btn = Button(
        top_frame,
        text="← Back",
        bg="#ff4d4d",
        fg="white",
        font=("Helvetica", 11, "bold"),
        relief="flat",
        cursor="hand2",
        padx=15,
        pady=5,
        command=products_window.destroy
    )

    back_btn.pack(side=LEFT)

    # =========================
    # SEARCH BAR
    # =========================

    search_frame = Frame(
        products_window,
        bg="#dff6f0"
    )

    search_frame.pack(pady=10)

    # CATEGORY FILTER BAR 
    category_frame=Frame(products_window,bg="#dff6f0")
    category_frame.pack(pady=10)
    selected_category = "ALL"
    categories = ["ALL","Electronics","Fashion","Furniture","Automobiles","Books","Other"]
    def filter_category(category):
        nonlocal selected_category
        selected_category=category
        load_products(search_entry.get())
    for category in categories :
        btn=Button(category_frame,text=category,bg="#002f34",fg="white",font=("Helvetica", 10, "bold"),relief="flat",cursor="hand2",padx=12,pady=5,command=lambda c=category: filter_category(c))
        btn.pack(side="left",padx=5)


    search_entry = Entry(
        search_frame,
        width=40,
        font=("Helvetica", 13),
        relief="solid",
        bd=1
    )

    search_entry.pack(
        side=LEFT,
        ipady=8,
        padx=10
    )

    search_btn = Button(
        search_frame,
        text="🔍 Search",
        bg="#2f6df6",
        fg="white",
        activebackground="#2457c5",
        activeforeground="white",
        font=("Helvetica", 12, "bold"),
        cursor="hand2",
        relief="flat",
        bd=0,
        padx=20,
        pady=8
    )

    search_btn.pack(side=LEFT)
    recent_btn=Button(search_frame,text="Recently Viewed",bg="#245de6",fg="white",font=("Helvetica",11,"bold"),relief="flat",cursor="hand2",padx=12,pady=8,command=lambda: open_recently_viewed())
    recent_btn.pack(side=LEFT,padx=10)

    # =========================
    # SCROLLABLE AREA
    # =========================

    canvas = Canvas(
        products_window,
        bg="#dff6f0",
        highlightthickness=0
    )

    scrollbar = Scrollbar(
        products_window,
        orient="vertical",
        command=canvas.yview
    )

    scrollable_frame = Frame(
        canvas,
        bg="#dff6f0"
    )

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window(
        (0, 0),
        window=scrollable_frame,
        anchor="nw"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # =========================
    # LOAD PRODUCTS
    # =========================

    def load_products(search_text=""):

        for widget in scrollable_frame.winfo_children():

            widget.destroy()

        products = get_products()
        if selected_category != "ALL":
            products = [p for p in products if p[7].lower() == selected_category.lower()]

        row = 0
        col = 0

        for product in products:
            product_id=product[0]

            title = product[1]

            if search_text.lower() not in title.lower():

                continue

            price = product[2]

            description = product[3]

            seller = product[4]

            image_path = product[5]
            status  = product[6]
            category=product[7]
            if status is None:
                status="available"

            # =========================
            # PRODUCT CARD
            # =========================

            card = Frame(
                scrollable_frame,
                bg="white",
                width=300,
                height=420,
                
                highlightthickness=0,
                bd=0,
                relief="flat"
            )

            card.grid(
                row=row,
                column=col,
                padx=15,
                pady=15,
                
            )

            card.grid_propagate(False)
            if current_user :
                card.bind("<Button-1>" , lambda e , p=product :track_view(p,current_user))

            # =========================
            # IMAGE SECTION
            # =========================

            image_frame = Frame(
                card,
                bg="#f8f8f8",
                width=280,
                height=200
            )

            image_frame.pack(
                pady=15
            )

            image_frame.pack_propagate(False)
            if current_user :
                image_frame.bind("<Button-1>" , lambda e , p=product :track_view(p,current_user))

            try:

                if image_path:

                    img = Image.open(image_path)

                    img = img.resize((280, 200),Image.LANCZOS)

                    img = ImageTk.PhotoImage(img)

                    image_label = Label(
                        image_frame,
                        image=img,
                        bg="#f5f5f5"
                    )

                    image_label.image = img

                    image_label.pack(fill="both",expand=True)

                else:

                    raise Exception("No Image")

            except:

                image_label = Label(
                    image_frame,
                    text="📷\n No Image Availaible",
                    bg="#f5f5f5",
                    fg="#999999",
                    font=("Helvetica", 13,"bold"),
                    justify="center"
                )

                image_label.pack(expand=True)

            # TITLE

            Label(
                card,
                text=title,
                font=("Helvetica", 14, "bold"),
                bg="white",
                fg="#002f34",
                wraplength=300,
                justify="left"
            ).pack(anchor="w",padx=15,pady=(10, 5))

            # PRICE

            Label(
                card,
                text=f"Rs. {price}",
                font=("Helvetica", 13, "bold"),
                bg="white",
                fg="#002f34"
            ).pack(anchor="w",padx=15,pady=(5,0))

            # DESCRIPTION

            Label(
                card,
                text=description,
                font=("Helvetica", 10),
                bg="white",
                fg="#444444",
                wraplength=250
            ).pack(anchor="w",padx=15,pady=(5,0))

            Label(card,text=f"📂 Category: {category}",font=("Helvetica",10,"bold"),bg="white",fg="#3a77ff").pack(pady=3)

            # SELLER

            Label(
                card,
                text=f"👤Seller: {seller}",
                font=("Helvetica", 10, "italic"),
                bg="white",
                fg="#7f8c8d"
            ).pack(anchor="w",padx=15,pady=5)
            if status == "sold":
                Label(card,text="SOLD OUT",bg="gray",fg="white",font=("Helvetica",12,"bold"),width=15).pack(pady=10)

              

            # BUY FUNCTION

            def buy_product(product_id,button,product_name=title):
                if status == "sold":
                    messagebox.showinfo("Sold Out", "This product is already sold out")
                    return
                
                confirm=messagebox.askyesno("Confirm Purchase",f"do you want to buy{product_name}?")

                if confirm:
                    mark_as_sold(product_id)
                    button.config(text="✓ SOLD",bg="gray",state=DISABLED)

                messagebox.showinfo(
                    "Purchase",
                    f"You bought {product_name}"
                )


            # BUY BUTTON

            buy_btn = Button(
                card,
                text="🛍 Buy Now",
                bg="#23e5db",
                fg="#002f34",
                activebackground="#1ccfc5",
                activeforeground="#002f34",
                font=("Helvetica", 11, "bold"),
                cursor="hand2",
                width=12,
                height=1,
                relief="flat",
                bd=0,
                
            )


            

            buy_btn.config(command=lambda pid=product_id, btn=buy_btn,name=title:buy_product(pid,btn,name))
            buy_btn.pack(side="left",padx=5)
            if status == "sold":
                buy_btn.config(text="SOLD", state=DISABLED, bg="gray")

            # DELETE FUNCTION

            def delete_this_product(card_frame=card):

                confirm = messagebox.askyesno(
                    "Delete Product",
                    "Are you sure you want to delete this product?"
                )

                if confirm:

                    card_frame.destroy()

                    messagebox.showinfo(
                        "Deleted",
                        "Product deleted successfully"
                    )

            # DELETE BUTTON

            delete_btn = Button(
                card,
                text="🗑 Delete",
                bg="#ff4d4f",
                fg="white",
                activebackground="#e63946",
                activeforeground="white",
                font=("Helvetica", 11, "bold"),
                cursor="hand2",
                width=12,
                height=1,
                relief="flat",
                bd=0,
                
                command=delete_this_product
            )

            delete_btn.pack(side="left",padx=5)

            col += 1

            if col == 2:

                col = 0

                row += 1


    def open_recently_viewed() :
        if not current_user :
            messagebox.showerror("Login Required !", "please Login First")
            return
        email=current_user[2]
        viewed=recently_viewed.get(email,[])
        if not viewed :
            messagebox.showinfo("Recently Viewed","You Have not Viewed Any Product Yet")
            return
        rv_window=Toplevel(window)
        rv_window.title("Recently Viewed Products")
        rv_window.geometry("650x550")
        rv_window.configure(bg="#dff6f0")
        Label(rv_window,text="Recently Window Products",font=("Helvetica",11,"bold"),bg="#dff6f0",fg="#002f34").pack(pady=15)
        for product in reversed(viewed) :
            tittle=product[1]
            price=product[2]
            Label(rv_window,text=f"{tittle} - Rs. {price}",font=("Helvetica",12),bg="white",fg="#002f34",anchor="w").pack(fill="x",padx=20,pady=5)

    # SEARCH FUNCTION

    def search_products():

        text = search_entry.get()

        load_products(text)

    search_btn.config(
        command=search_products
    )

    load_products()

# =========================
# REGISTER WINDOW
# =========================

def open_register():

    register_window = Toplevel(window)

    register_window.title("Register")

    register_window.geometry("400x400")

    register_window.configure(bg="#dff6f0")

    heading = Label(
        register_window,
        text="Create Your Account",
        font=("Helvetica", 20, "bold"),
        bg="#dff6f0",
        fg="#002f34"
    )

    heading.pack(pady=20)

    Label(
        register_window,
        text="Name",
        font=("Helvetica", 12, "bold"),
        bg="#dff6f0"
    ).pack()

    name_entry = Entry(register_window, width=30)
    name_entry.pack(pady=8)

    Label(
        register_window,
        text="Email",
        font=("Helvetica", 12, "bold"),
        bg="#dff6f0"
    ).pack()

    email_entry = Entry(register_window, width=30)
    email_entry.pack(pady=8)

    Label(
        register_window,
        text="Password",
        font=("Helvetica", 12, "bold"),
        bg="#dff6f0"
    ).pack()

    password_entry = Entry(
        register_window,
        width=30,
        show="*"
    )

    password_entry.pack(pady=8)

    def save_user():

        name = name_entry.get()
        email = email_entry.get()
        password = password_entry.get()

        if name == "" or email == "" or password == "":

            messagebox.showerror(
                "Error",
                "Please fill all fields"
            )

            return

        result=register_user(name, email, password)

        if result :
            messagebox.showinfo("Success","Succesfully registered !!")
            register_window.destroy()
        else :
            messagebox.showerror("Error","Email already exists !! ")

    register_btn = Label(
        register_window,
        text="Register",
        bg="#00a49f",
        fg="white",
        font=("Helvetica", 13, "bold"),
        width=20,
        height=2,
        cursor="hand2"
    )

    register_btn.pack(pady=20)

    register_btn.bind(
        "<Button-1>",
        lambda e: save_user()
    )

# =========================
# LOGIN WINDOW
# =========================

def open_login():

    login_window = Toplevel(window)

    login_window.title("Login")

    login_window.geometry("400x350")

    login_window.configure(bg="#dff6f0")

    heading = Label(
        login_window,
        text="Login To Your Account",
        font=("Helvetica", 20, "bold"),
        bg="#dff6f0",
        fg="#002f34"
    )

    heading.pack(pady=20)

    Label(
        login_window,
        text="Email",
        font=("Helvetica", 12, "bold"),
        bg="#dff6f0"
    ).pack()

    email_entry = Entry(login_window, width=30)
    email_entry.pack(pady=8)

    Label(
        login_window,
        text="Password",
        font=("Helvetica", 12, "bold"),
        bg="#dff6f0"
    ).pack()

    password_entry = Entry(
        login_window,
        width=30,
        show="*"
    )

    password_entry.pack(pady=8)

    def login_user_gui():

        email = email_entry.get()
        password = password_entry.get()

        user = login_user(email, password)

        if user:

            global current_user
            current_user=user
            login_window.destroy()
            open_dashboard(user)

        else:

            messagebox.showerror(
                "Error",
                "Invalid Email or Password"
            )

    login_btn = Label(
        login_window,
        text="Login",
        bg="#3a77ff",
        fg="white",
        font=("Helvetica", 13, "bold"),
        width=20,
        height=2,
        cursor="hand2"
    )

    login_btn.pack(pady=20)

    login_btn.bind(
        "<Button-1>",
        lambda e: login_user_gui()
    )

# =========================
# DELETE ACCOUNT WINDOW
# =========================

def open_delete_account():

    delete_window = Toplevel(window)

    delete_window.title("Delete Account")

    delete_window.geometry("400x350")

    delete_window.configure(bg="#dff6f0")

    heading = Label(
        delete_window,
        text="Delete Your Account",
        font=("Helvetica", 20, "bold"),
        bg="#dff6f0",
        fg="red"
    )

    heading.pack(pady=20)

    Label(
        delete_window,
        text="Email",
        font=("Helvetica", 12, "bold"),
        bg="#dff6f0"
    ).pack()

    email_entry = Entry(delete_window, width=30)
    email_entry.pack(pady=8)

    Label(
        delete_window,
        text="Password",
        font=("Helvetica", 12, "bold"),
        bg="#dff6f0"
    ).pack()

    password_entry = Entry(
        delete_window,
        width=30,
        show="*"
    )

    password_entry.pack(pady=8)

    def delete_account():

        email = email_entry.get()
        password = password_entry.get()

        deleted = delete_user(email, password)

        if deleted:

            messagebox.showinfo(
                "Success",
                "Account Deleted Successfully"
            )

            delete_window.destroy()

        else:

            messagebox.showerror(
                "Error",
                "Invalid Email or Password"
            )

    delete_btn = Label(
        delete_window,
        text="Delete Account",
        bg="#ff4d4d",
        fg="white",
        font=("Helvetica", 13, "bold"),
        width=20,
        height=2,
        cursor="hand2"
    )

    delete_btn.pack(pady=20)

    delete_btn.bind(
        "<Button-1>",
        lambda e: delete_account()
    )

# =========================
# MAIN WINDOW BUTTONS
# =========================

register_btn = Label(
    main_frame,
    text="Register",
    bg="#00a49f",
    fg="white",
    font=("Helvetica", 14, "bold"),
    width=22,
    height=2,
    cursor="hand2"
)

register_btn.pack(pady=10)

register_btn.bind(
    "<Button-1>",
    lambda e: open_register()
)

login_btn = Label(
    main_frame,
    text="Login",
    bg="#3a77ff",
    fg="white",
    font=("Helvetica", 14, "bold"),
    width=22,
    height=2,
    cursor="hand2"
)

login_btn.pack(pady=10)

login_btn.bind(
    "<Button-1>",
    lambda e: open_login()
)

delete_account_btn = Label(
    main_frame,
    text="Delete Account",
    bg="#ff4d4d",
    fg="white",
    font=("Helvetica", 14, "bold"),
    width=22,
    height=2,
    cursor="hand2"
)

delete_account_btn.pack(pady=10)

delete_account_btn.bind(
    "<Button-1>",
    lambda e: open_delete_account()
)

# =========================
# RUN APP
# =========================
home_btn.bind(
    "<Button-1>",
    lambda e: open_home()
)

sell_btn.bind(
    "<Button-1>",
    lambda e: open_sell()
)

products_btn.bind(
    "<Button-1>",
    lambda e: open_products()
)

logout_btn.bind(
    "<Button-1>",
    lambda e: logout()
)
window.mainloop()
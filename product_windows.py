from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import state
from product import add_product, get_products, delete_product, mark_as_sold
from category_helpers import category_tree, get_subcategories


def open_add_product(window, user):

    add_window = Toplevel(window)
    add_window.title("Sell Product")
    add_window.geometry("500x900")
    add_window.configure(bg="#dff6f0")
    add_window.grab_set()

    seller_name = user[1]

    heading = Label(add_window,text="Sell Your Product",font=("Helvetica", 22, "bold"),bg="#dff6f0",fg="#002f34")
    heading.pack(pady=(20,25))

    Label(add_window,text="Product Title",font=("Helvetica", 12, "bold"),bg="#dff6f0").pack(pady=(0,5))
    title_entry = Entry(add_window,width=35,font=("Helvetica", 11))
    title_entry.pack(ipady=8,pady=(5,20))

    Label(add_window,text="Price",font=("Helvetica", 12, "bold"),bg="#dff6f0").pack(pady=(0,5))
    price_entry = Entry(add_window,width=35,font=("Helvetica", 11))
    price_entry.pack(ipady=8,pady=(5,20))

    Label(add_window,text="Category",font=("Helvetica",12,"bold"),bg="#dff6f0").pack(pady=(0,5))
    category_var=StringVar()
    category_var.set("Electronics")
    category_menu=OptionMenu(add_window,category_var,"Electronics","Fashion","Furniture","Automobiles","Books","other")
    category_menu.config(width=20,font=("helvetica",11))
    category_menu.pack(pady=(5,20))

    subcategory_var = StringVar()
    Label(add_window, text="Sub-Category", font=("Helvetica", 12, "bold"), bg="#dff6f0").pack(pady=(0, 5))
    subcategory_menu = OptionMenu(add_window, subcategory_var, "")
    subcategory_menu.config(width=20, font=("helvetica", 11))
    subcategory_menu.pack(pady=(5, 20))

    def update_subcategories(*args):
        subs = get_subcategories(category_var.get())
        menu = subcategory_menu["menu"]
        menu.delete(0, "end")
        for sub in subs:
            menu.add_command(label=sub, command=lambda value=sub: subcategory_var.set(value))
        if subs:
            subcategory_var.set(subs[0])

    category_var.trace_add("write", update_subcategories)
    update_subcategories()

    Label(add_window,text="Description",font=("Helvetica", 12, "bold"),bg="#dff6f0").pack(pady=(0,5))
    desc_text = Text(add_window,width=35,height=6,font=("Helvetica", 11))
    desc_text.pack(pady=(5,20))

    image_path = StringVar()

    def upload_image():
        file = filedialog.askopenfilename(
            parent=add_window,
            title="Select Product Image",
            filetypes=[("PNG Files", "*.png"),("JPG Files", "*.jpg"),("JPEG Files", "*.jpeg")]
        )
        if file:
            image_path.set(file)
            image_label.config(text="✅ Image Selected")

    upload_btn = Label(add_window,text="📷 Upload Image",bg="#3a77ff",fg="white",font=("Helvetica", 12, "bold"),width=20,height=2,cursor="hand2")
    upload_btn.pack(pady=(5,8))
    upload_btn.bind("<Button-1>",lambda e: upload_image())

    image_label = Label(add_window,text="No Image Selected",font=("Helvetica", 10),bg="#dff6f0",fg="gray")
    image_label.pack(pady=(0,20))

    def save_product():
        title = title_entry.get()
        price = price_entry.get()
        description = desc_text.get("1.0", END)
        category=category_var.get()
        subcategory=subcategory_var.get()

        if title == "" or price == "" or description.strip() == "":
            messagebox.showerror("Error","Please fill all fields")
            return
        try :
            price_value = float(price)
            if price_value <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Price must be a valid positive number")
            return
        add_product(title,price,description,seller_name,image_path.get(),category,subcategory)
        messagebox.showinfo("Success","Product Added Successfully")
        add_window.destroy()

    save_btn = Label(add_window,text="💰 Sell Product",bg="#00a49f",fg="white",font=("Helvetica", 13, "bold"),width=22,height=2,cursor="hand2")
    save_btn.pack(pady=(20,10))
    save_btn.bind("<Button-1>",lambda e: save_product())


def open_products_window(window, previous_window):
    selected_category = "ALL"
    current_page=0
    PAGE_SIZE=6

    products_window = Toplevel(window)
    products_window.title("All Products")
    products_window.geometry("1300x800")
    products_window.minsize(1200,750)
    products_window.configure(bg="#dff6f0")

    heading = Label(products_window,text="Available Products",font=("Helvetica", 28, "bold"),bg="#dff6f0",fg="#002f34")
    heading.pack(pady=20)

    top_frame = Frame(products_window,bg="#dff6f0")
    top_frame.pack(fill="x", padx=20)

    def go_back():
        products_window.destroy()
        if previous_window is not None :
            previous_window.deiconify()

    back_btn = Button(top_frame,text="← Back",bg="#ff4d4d",fg="white",font=("Helvetica", 11, "bold"),relief="flat",cursor="hand2",padx=15,pady=5,command=go_back)
    back_btn.pack(side=LEFT)

    main_content = Frame(products_window, bg="#dff6f0")
    main_content.pack(fill="both", expand=True)
    sidebar = Frame(main_content, bg="#002f34", width=180)
    sidebar.pack(side=LEFT, fill="y")
    sidebar.pack_propagate(False)
    Label(sidebar, text="FEATURES", bg="#002f34", fg="#7f8c8d", font=("Helvetica", 10, "bold")).pack(pady=(20, 10))
    recent_btn = Button(sidebar, text="🕑 Recently Viewed", bg="#245de6", fg="white", font=("Helvetica", 10, "bold"), relief="flat", cursor="hand2", padx=10, pady=10, command=lambda: open_recently_viewed())
    recent_btn.pack(fill="x", padx=15, pady=5)
    undo_btn = Button(sidebar, text="↩ Undo Delete", bg="#245de6", fg="white", font=("Helvetica", 10, "bold"), relief="flat", cursor="hand2", padx=10, pady=10, command=lambda: undo_last_delete())
    undo_btn.pack(fill="x", padx=15, pady=5)
    content_area = Frame(main_content, bg="#dff6f0")
    content_area.pack(side=LEFT, fill="both", expand=True)
    search_frame = Frame(content_area,bg="#dff6f0")
    search_frame.pack(pady=10)

    category_frame=Frame(content_area,bg="#dff6f0")
    category_frame.pack(pady=10)
    selected_category = "ALL"
    categories = ["ALL"] + [node.name for node in category_tree.children]
    selected_subcategory="ALL"
    subcategory_frame=Frame(content_area,bg="#dff6f0")
    subcategory_frame.pack(pady=(0,10))

    def filter_subcategory(subcategory) :
        nonlocal selected_subcategory
        selected_subcategory=subcategory
        load_products(search_entry.get())

    def show_subcategory_buttons(category_name) :
        for widget in subcategory_frame.winfo_children() :
            widget.destroy()
        subs=get_subcategories(category_name)
        if not subs :
            return
        Button(subcategory_frame, text="ALL", bg="#3a77ff", fg="white", font=("Helvetica", 9, "bold"), relief="flat", cursor="hand2", padx=10, pady=4, command=lambda: filter_subcategory("ALL")).pack(side="left", padx=3)
        for sub in subs :
            Button(subcategory_frame, text=sub, bg="#3a77ff", fg="white", font=("Helvetica", 9, "bold"), relief="flat", cursor="hand2", padx=10, pady=4, command=lambda s=sub: filter_subcategory(s)).pack(side="left", padx=3)

    def filter_category(category):
        nonlocal selected_category, selected_subcategory
        selected_category = category
        selected_subcategory = "ALL"
        show_subcategory_buttons(category)
        load_products(search_entry.get())

    for category in categories:
        btn=Button(category_frame,text=category,bg="#002f34",fg="white",font=("Helvetica", 10, "bold"),relief="flat",cursor="hand2",padx=12,pady=5,command=lambda c=category: filter_category(c))
        btn.pack(side="left",padx=5)

    search_entry = Entry(search_frame,width=40,font=("Helvetica", 13),relief="solid",bd=1)
    search_entry.pack(side=LEFT,ipady=8,padx=10)

    search_btn = Button(search_frame,text="🔍 Search",bg="#2f6df6",fg="white",activebackground="#2457c5",activeforeground="white",font=("Helvetica", 12, "bold"),cursor="hand2",relief="flat",bd=0,padx=20,pady=8)
    search_btn.pack(side=LEFT)

    canvas = Canvas(content_area,bg="#dff6f0",highlightthickness=0)
    scrollbar = Scrollbar(content_area,orient="vertical",command=canvas.yview)
    scrollable_frame = Frame(canvas,bg="#dff6f0")

    scrollable_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0),window=scrollable_frame,anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left",fill="both",expand=True)
    scrollbar.pack(side="right",fill="y")

    def load_products(search_text=""):
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        nonlocal current_page

        products = get_products()
        if selected_category != "ALL":
            products = [p for p in products if p.category.lower() == selected_category.lower()]
        if search_text :
            products = [p for p in products if search_text.lower() in p.title.lower()]
        total_pages = max(1, (len(products) + PAGE_SIZE - 1) // PAGE_SIZE)
        current_page = min(current_page, total_pages - 1)
        start = current_page * PAGE_SIZE
        products = products[start:start + PAGE_SIZE]

        row = 0
        col = 0

        for product in products:
            product_id=product.id
            title = product.title
            price = product.price
            description = product.description
            seller = product.seller
            image_path = product.image
            status  = product.status
            category=product.category

            card = Frame(scrollable_frame,bg="white",width=300,height=420,highlightthickness=1,highlightbackground="#e0e0e0",bd=0,relief="flat")
            card.grid(row=row,column=col,padx=15,pady=15,)
            card.grid_propagate(False)
            if state.current_user :
                card.bind("<Button-1>" , lambda e , p=product :state.track_view(p,state.current_user))

            image_frame = Frame(card,bg="#f8f8f8",width=280,height=200)
            image_frame.pack(pady=15)
            image_frame.pack_propagate(False)
            if state.current_user :
                image_frame.bind("<Button-1>" , lambda e , p=product :state.track_view(p,state.current_user))

            try:
                if image_path:
                    img = Image.open(image_path)
                    img = img.resize((280, 200),Image.LANCZOS)
                    img = ImageTk.PhotoImage(img)
                    image_label = Label(image_frame,image=img,bg="#f5f5f5")
                    image_label.image = img
                    image_label.pack(fill="both",expand=True)
                else:
                    raise Exception("No Image")
            except Exception:
                image_label = Label(image_frame, text="📷\nNo Image Available", bg="#f5f5f5", fg="#b0b0b0", font=("Helvetica", 12), justify="center")
                image_label.pack(expand=True)

            Label(card,text=title,font=("Helvetica", 14, "bold"),bg="white",fg="#002f34",wraplength=300,justify="left").pack(anchor="w",padx=15,pady=(10, 5))
            Label(card,text=f"Rs. {price}",font=("Helvetica", 13, "bold"),bg="white",fg="#002f34").pack(anchor="w",padx=15,pady=(5,0))
            Label(card,text=description,font=("Helvetica", 10),bg="white",fg="#444444",wraplength=250).pack(anchor="w",padx=15,pady=(5,0))
            Label(card,text=f"📂 Category: {category}",font=("Helvetica",10,"bold"),bg="white",fg="#3a77ff").pack(pady=3)
            Label(card,text=f"👤Seller: {seller}",font=("Helvetica", 10, "italic"),bg="white",fg="#7f8c8d").pack(anchor="w",padx=15,pady=5)
            if status == "sold":
                Label(card,text="SOLD OUT",bg="gray",fg="white",font=("Helvetica",12,"bold"),width=15).pack(pady=10)

            def buy_product(product_id,button,product_name=title):
                if status == "sold":
                    messagebox.showinfo("Sold Out", "This product is already sold out")
                    return
                confirm=messagebox.askyesno("Confirm Purchase",f"do you want to buy {product_name}?")
                if confirm:
                    mark_as_sold(product_id)
                    button.config(text="✓ SOLD",bg="gray",state=DISABLED)
                    messagebox.showinfo("Purchase",f"You bought {product_name}")

            buy_btn = Button(card,text="🛍 Buy Now",bg="#23e5db",fg="#002f34",activebackground="#1ccfc5",activeforeground="#002f34",font=("Helvetica", 11, "bold"),cursor="hand2",width=12,height=1,relief="flat",bd=0,)
            buy_btn.config(command=lambda pid=product_id, btn=buy_btn,name=title:buy_product(pid,btn,name))
            buy_btn.pack(side="left",padx=5)
            if status == "sold":
                buy_btn.config(text="SOLD", state=DISABLED, bg="gray")

            def delete_this_product(card_frame=card,pid=product_id,prod=product):
                if not state.current_user :
                    messagebox.showerror("Stopped !! ", "Please Login First")
                    return
                if prod.seller != state.current_user[1] :
                    messagebox.showerror("Not Deleted","You can only delete Your Own Product")
                    return
                confirm = messagebox.askyesno("Delete Product","Are you sure you want to delete this product?")
                if confirm:
                    delete_product(pid)
                    state.push_deleted(prod,state.current_user)
                    card_frame.destroy()
                    messagebox.showinfo("Deleted","Product deleted successfully")

            delete_btn = Button(card,text="🗑 Delete",bg="#ff4d4f",fg="white",activebackground="#e63946",activeforeground="white",font=("Helvetica", 11, "bold"),cursor="hand2",width=12,height=1,relief="flat",bd=0,command=delete_this_product)
            delete_btn.pack(side="left",padx=5)

            col += 1
            if col == 2:
                col = 0
                row += 1

    def open_recently_viewed() :
        if not state.current_user :
            messagebox.showerror("Login Required !", "please Login First")
            return
        email=state.current_user[2]
        viewed=state.recently_viewed.get(email,[])
        if not viewed :
            messagebox.showinfo("Recently Viewed","You Have not Viewed Any Product Yet")
            return
        rv_window=Toplevel(window)
        rv_window.title("Recently Viewed Products")
        rv_window.geometry("650x550")
        rv_window.configure(bg="#dff6f0")
        Label(rv_window,text="Recently Window Products",font=("Helvetica",11,"bold"),bg="#dff6f0",fg="#002f34").pack(pady=15)
        for product in reversed(viewed) :
            title=product.title
            price=product.price
            Label(rv_window,text=f"{title} - Rs. {price}",font=("Helvetica",12),bg="white",fg="#002f34",anchor="w").pack(fill="x",padx=20,pady=5)

    def undo_last_delete() :
        if not state.current_user :
            messagebox.showerror("Login Required !!" , "Please Login First")
            return
        restored=state.undo_delete(state.current_user)
        if restored is None :
            messagebox.showinfo("Empty","Nothing to undo")
            return
        messagebox.showinfo("Successfull","Product Restored !!")
        load_products()

    def search_products():
        text = search_entry.get()
        load_products(text)

    search_btn.config(command=search_products)

    nav_frame = Frame(content_area, bg="#dff6f0")
    nav_frame.pack(pady=10)

    def prev_page():
        nonlocal current_page
        if current_page > 0:
            current_page -= 1
            load_products(search_entry.get())

    def next_page():
        nonlocal current_page
        current_page += 1
        load_products(search_entry.get())

    Button(nav_frame, text="← Prev", command=prev_page, bg="#002f34", fg="white", relief="flat", padx=15, pady=5).pack(side=LEFT, padx=5)
    Button(nav_frame, text="Next →", command=next_page, bg="#002f34", fg="white", relief="flat", padx=15, pady=5).pack(side=LEFT, padx=5)

    load_products()
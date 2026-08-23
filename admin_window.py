from tkinter import *
from tkinter import ttk
import os
import sqlite3
from utils import create_toplevel_window

def get_admin_stats():
    """Database se quick stats fetch karta hai"""
    db_path = os.path.join(os.path.dirname(__file__), "database", "olx.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Total Users count
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='user'")
    users_count = cursor.fetchone()[0]
    
    # Total Products count
    cursor.execute("SELECT COUNT(*) FROM products")
    products_count = cursor.fetchone()[0]
    
    # Sold Products count
    cursor.execute("SELECT COUNT(*) FROM products WHERE status='sold'")
    sold_count = cursor.fetchone()[0]
    
    conn.close()
    return users_count, products_count, sold_count

def open_admin_panel(window):
    admin_win = create_toplevel_window(window, "OLX Admin Control Panel", "1200x700")
    
    # === SIDEBAR (Dark Teal) ===
    sidebar = Frame(admin_win, bg="#002f34", width=250)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)
    
    Label(sidebar, text="OLX ADMIN", font=("Helvetica", 20, "bold"), bg="#002f34", fg="white").pack(pady=(30, 40))
    
    # 🟢 FIX 1: Sidebar buttons ke commands add kiye (All Listings check karne ke liye)
    def open_all_listings():
        from product_windows import open_products_window
        open_products_window(window, admin_win)

    Button(sidebar, text="📊 Dashboard Overview", bg="#00a49f", fg="white", font=("Helvetica", 12, "bold"), bd=0, anchor="w", padx=20, pady=10, cursor="hand2").pack(fill="x")
    Button(sidebar, text="📦 All Listings", bg="#002f34", fg="white", font=("Helvetica", 12), bd=0, activebackground="#00a49f", activeforeground="white", anchor="w", padx=20, pady=10, cursor="hand2", command=open_all_listings).pack(fill="x")
    
    # Logout Button (Sidebar ke bottom par)
    def admin_logout():
        import state
        state.current_user = None
        admin_win.destroy()
        
    Button(sidebar, text="🚪 Logout", bg="#002f34", fg="#ff4d4d", font=("Helvetica", 12, "bold"), bd=0, activebackground="#ff4d4d", activeforeground="white", anchor="w", padx=20, pady=10, cursor="hand2", command=admin_logout).pack(side="bottom", fill="x", pady=20)

    # === MAIN CONTENT AREA (Light Teal) ===
    main_content = Frame(admin_win, bg="#dff6f0")
    main_content.pack(side="left", fill="both", expand=True)
    
    # Header
    header_frame = Frame(main_content, bg="#dff6f0")
    header_frame.pack(fill="x", padx=30, pady=(30, 10))
    Label(header_frame, text="Platform Control Center", font=("Helvetica", 24, "bold"), bg="#dff6f0", fg="#002f34").pack(anchor="w")
    Label(header_frame, text="Welcome back, Super Admin Arsalan.", font=("Helvetica", 12), bg="#dff6f0", fg="#7f8c8d").pack(anchor="w", pady=(5, 0))
    
    # === METRICS CARDS ===
    stats_frame = Frame(main_content, bg="#dff6f0")
    stats_frame.pack(fill="x", padx=30, pady=20)
    
    u_count, p_count, s_count = get_admin_stats()
    
    def create_stat_card(parent, title, value):
        card = Frame(parent, bg="white", highlightthickness=1, highlightbackground="#e0e0e0", padx=20, pady=15)
        Label(card, text=title, font=("Helvetica", 11), bg="white", fg="#7f8c8d").pack(anchor="w")
        Label(card, text=str(value), font=("Helvetica", 26, "bold"), bg="white", fg="#002f34").pack(anchor="w", pady=(5,0))
        return card
        
    create_stat_card(stats_frame, "Total Registered Users", u_count).pack(side="left", fill="x", expand=True, padx=(0, 10))
    create_stat_card(stats_frame, "Active Product Listings", p_count).pack(side="left", fill="x", expand=True, padx=10)
    create_stat_card(stats_frame, "Sold Items", s_count).pack(side="left", fill="x", expand=True, padx=(10, 0))

    # === USERS TABLE ===
    table_frame = Frame(main_content, bg="white", highlightthickness=1, highlightbackground="#e0e0e0")
    table_frame.pack(fill="both", expand=True, padx=30, pady=(10, 30))
    
    Label(table_frame, text="Recent User Signups", font=("Helvetica", 16, "bold"), bg="white", fg="#002f34").pack(anchor="w", padx=20, pady=15)
    
    # 🟢 FIX 2: Naya frame scrollbar aur table ke liye taake button neechay aa sakay
    tree_frame = Frame(table_frame, bg="white")
    tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

    # 🟢 FIX 3: Scrollbar add kiya
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side="right", fill="y")

    # Styling the Treeview (Table)
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"), background="#dff6f0", foreground="#002f34")
    style.configure("Treeview", font=("Helvetica", 10), rowheight=35)
    style.map("Treeview", background=[("selected", "#00a49f")])
    
    columns = ("id", "name", "email", "role")
    
    # Table ko height di aur scrollbar ke sath connect kiya
    user_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8, yscrollcommand=tree_scroll.set)
    tree_scroll.config(command=user_tree.yview)
    
    user_tree.heading("id", text="User ID")
    user_tree.heading("name", text="Name")
    user_tree.heading("email", text="Email")
    user_tree.heading("role", text="Role")
    
    user_tree.column("id", width=80, anchor="center")
    user_tree.column("name", width=200)
    user_tree.column("email", width=250)
    user_tree.column("role", width=100, anchor="center")
    
    user_tree.pack(side="left", fill="both", expand=True)
    
    # Fetch and display users in table
    db_path = os.path.join(os.path.dirname(__file__), "database", "olx.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, role FROM users")
    
    for row in cursor.fetchall():
        user_tree.insert("", "end", values=row)
        
    conn.close()

    # 🟢 FIX 4: Delete Button ki alignment theek ki aur table_frame mein pack kiya
    def delete_selected_user():
        selected_item = user_tree.selection()
        if not selected_item:
            from tkinter import messagebox
            messagebox.showwarning("Selection Error", "Please select a user to delete.")
            return
            
        user_id = user_tree.item(selected_item)['values'][0]
        user_role = user_tree.item(selected_item)['values'][3]
        user_name = user_tree.item(selected_item)['values'][1]
        
        if str(user_role).lower() == 'admin':
            from tkinter import messagebox
            messagebox.showerror("Action Denied", "You cannot delete an Admin account!")
            return
            
        from tkinter import messagebox
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete user: {user_name}?")
        
        if confirm:
            db_path = os.path.join(os.path.dirname(__file__), "database", "olx.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
            cursor.execute("DELETE FROM products WHERE seller=?", (user_name,))
            conn.commit()
            conn.close()
            
            user_tree.delete(selected_item)
            messagebox.showinfo("Success", f"User {user_name} and their products have been deleted.")

    delete_btn = Button(table_frame, text="🗑 Delete Selected User", bg="#ff4d4d", fg="white", font=("Helvetica", 11, "bold"), bd=0, activebackground="#cc0000", activeforeground="white", cursor="hand2", padx=15, pady=8, command=delete_selected_user)
    delete_btn.pack(pady=(0, 20))
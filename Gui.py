# =========================
# IMPORTS
# =========================

from tkinter import *
from tkinter import messagebox
import os
import state
from auth_windows import open_register, open_login, open_delete_account
from dashboard_window import open_dashboard
from product_windows import open_add_product, open_products_window

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
sell_btn.bind("<Enter>", navbar_enter)
sell_btn.bind("<Leave>", navbar_leave)

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
    if state.current_user:
        open_add_product(window, state.current_user)
    else:
        messagebox.showerror("Login Required", "Please login first")

def open_products():
    open_products_window(window, None)

def logout():
    state.current_user = None
    for widget in window.winfo_children():
        if isinstance(widget, Toplevel):
            widget.destroy()
    messagebox.showinfo("Logout", "Logged out successfully")


home_btn.bind("<Button-1>", lambda e: open_home())
sell_btn.bind("<Button-1>", lambda e: open_sell())
products_btn.bind("<Button-1>", lambda e: open_products())
logout_btn.bind("<Button-1>", lambda e: logout())

# =========================
# MAIN FRAME
# =========================

main_frame = Frame(window, bg="#dff6f0")
main_frame.pack(expand=True)

current_folder = os.path.dirname(__file__)
logo_path = os.path.join(current_folder, "logo.png")
logo = PhotoImage(file=logo_path)
logo = logo.subsample(15, 15)

logo_label = Label(main_frame,image=logo,bg="#dff6f0")
logo_label.pack(pady=20)

title = Label(main_frame,text="Buy & Sell Anything Easily",font=("Helvetica", 30, "bold"),bg="#dff6f0",fg="#002f34")
title.pack(pady=10)

subtitle = Label(main_frame,text="Pakistan's Modern Desktop Marketplace",font=("Helvetica", 12),bg="#dff6f0",fg="gray")
subtitle.pack(pady=(0, 30))

# =========================
# MAIN WINDOW BUTTONS
# =========================

register_btn = Label(main_frame,text="Register",bg="#00a49f",fg="white",font=("Helvetica", 14, "bold"),width=22,height=2,cursor="hand2")
register_btn.pack(pady=10)
register_btn.bind("<Button-1>", lambda e: open_register(window))

login_btn = Label(main_frame,text="Login",bg="#3a77ff",fg="white",font=("Helvetica", 14, "bold"),width=22,height=2,cursor="hand2")
login_btn.pack(pady=10)
login_btn.bind("<Button-1>", lambda e: open_login(window))

delete_account_btn = Label(main_frame,text="Delete Account",bg="#dff6f0",fg="#6b7280",font=("Helvetica", 10, "underline"),cursor="hand2")
delete_account_btn.pack(pady=(25,5))
delete_account_btn.bind("<Button-1>", lambda e: open_delete_account(window))

# =========================
# RUN APP
# =========================

window.mainloop()
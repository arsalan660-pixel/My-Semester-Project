from tkinter import *
from tkinter import messagebox
import state
from auth import register_user, login_user, delete_user


def open_register(window):

    register_window = Toplevel(window)
    register_window.title("Register")
    register_window.geometry("400x480")
    register_window.configure(bg="#dff6f0")

    heading = Label(register_window,text="Create Your Account",font=("Helvetica", 20, "bold"),bg="#dff6f0",fg="#002f34")
    heading.pack(pady=(20,25))

    Label(register_window,text="Name",font=("Helvetica", 12, "bold"),bg="#dff6f0").pack(pady=(0,5))
    name_entry = Entry(register_window, width=30)
    name_entry.pack(ipady=8,pady=(5,25))

    Label(register_window,text="Email",font=("Helvetica", 12, "bold"),bg="#dff6f0").pack(pady=(0,5))
    email_entry = Entry(register_window, width=30)
    email_entry.pack(ipady=8,pady=(5,25))

    Label(register_window,text="Password",font=("Helvetica", 12, "bold"),bg="#dff6f0").pack(pady=(0,5))
    password_entry = Entry(register_window,width=30,show="*")
    password_entry.pack(ipady=8,pady=(5,20))

    def save_user():
        name = name_entry.get()
        email = email_entry.get()
        password = password_entry.get()

        if name == "" or email == "" or password == "":
            messagebox.showerror("Error","Please fill all fields")
            return

        result=register_user(name, email, password)

        if result :
            messagebox.showinfo("Success","Succesfully registered !!")
            register_window.destroy()
        else :
            messagebox.showerror("Error","Email already exists !! ")

    register_btn = Label(register_window,text="Register",bg="#00a49f",fg="white",font=("Helvetica", 13, "bold"),width=20,height=2,cursor="hand2")
    register_btn.pack(pady=(30,10))
    register_btn.bind("<Button-1>", lambda e: save_user())


def open_login(window):

    login_window = Toplevel(window)
    login_window.title("Login")
    login_window.geometry("420x460")
    login_window.configure(bg="#dff6f0")

    heading = Label(login_window, text="OLX Clone", font=("Helvetica", 20, "bold"),
                     bg="#dff6f0", fg="#002f34")
    heading.pack(pady=(30, 20))

    card = Frame(login_window, bg="white", highlightthickness=1,
                 highlightbackground="#e0e0e0", bd=0)
    card.pack(padx=30, pady=(0, 20), fill="x")

    inner = Frame(card, bg="white")
    inner.pack(padx=25, pady=25, fill="x")

    Label(inner, text="Email", font=("Helvetica", 11, "bold"), bg="white", fg="#002f34").pack(anchor="w")
    saved_email = state.get_saved_user_email()
    email_entry = Entry(inner, width=28, font=("Helvetica", 11), relief="solid", bd=1)
    email_entry.pack(ipady=6, pady=(4, 16), fill="x")
    if saved_email:
        email_entry.insert(0, saved_email)

    Label(inner, text="Password", font=("Helvetica", 11, "bold"), bg="white", fg="#002f34").pack(anchor="w")
    password_entry = Entry(inner, width=28, font=("Helvetica", 11), show="*", relief="solid", bd=1)
    password_entry.pack(ipady=6, pady=(4, 12), fill="x")

    remember_var = BooleanVar(value=bool(saved_email))
    remember_check = Checkbutton(inner, text="Remember Me", variable=remember_var,
                                  bg="white", font=("Helvetica", 9))
    remember_check.pack(anchor="w", pady=(0, 18))

    def login_user_gui():
        email = email_entry.get()
        password = password_entry.get()

        user = login_user(email, password)

        if user:
            state.current_user = user
            if remember_var.get():
                state.save_user_email(email)
            else:
                state.save_user_email("")
            login_window.destroy()
            from dashboard_window import open_dashboard
            open_dashboard(window, user)
        else:
            messagebox.showerror("Error", "Invalid Email or Password")

    login_btn = Button(inner, text="Login", bg="#3a77ff", fg="white",
                        activebackground="#245de6", activeforeground="white",
                        font=("Helvetica", 12, "bold"), relief="flat", bd=0,
                        cursor="hand2", pady=10, command=login_user_gui)
    login_btn.pack(fill="x")

    create_account_label = Label(login_window, text="Don't have an account? Register",
                                  bg="#dff6f0", fg="#6b7280", font=("Helvetica", 9, "underline"),
                                  cursor="hand2")
    create_account_label.pack(pady=(5, 0))
    create_account_label.bind("<Button-1>", lambda e: (login_window.destroy(), open_register(window)))


def open_delete_account(window):

    delete_window = Toplevel(window)
    delete_window.title("Delete Account")
    delete_window.geometry("400x350")
    delete_window.configure(bg="#dff6f0")

    heading = Label(delete_window,text="Delete Your Account",font=("Helvetica", 20, "bold"),bg="#dff6f0",fg="red")
    heading.pack(pady=(20,25))

    Label(delete_window,text="Email",font=("Helvetica", 12, "bold"),bg="#dff6f0").pack(pady=(0,5))
    email_entry = Entry(delete_window, width=30)
    email_entry.pack(ipady=8,pady=(5,20))

    Label(delete_window,text="Password",font=("Helvetica", 12, "bold"),bg="#dff6f0").pack(pady=(0,5))
    password_entry = Entry(delete_window,width=30,show="*")
    password_entry.pack(ipady=8,pady=(5,20))

    def delete_account():
        email = email_entry.get()
        password = password_entry.get()

        deleted = delete_user(email, password)

        if deleted:
            messagebox.showinfo("Success","Account Deleted Successfully")
            delete_window.destroy()
        else:
            messagebox.showerror("Error","Invalid Email or Password")

    delete_btn = Label(delete_window,text="Delete Account",bg="#ff4d4d",fg="white",font=("Helvetica", 13, "bold"),width=20,height=2,cursor="hand2")
    delete_btn.pack(pady=(30,10))
    delete_btn.bind("<Button-1>", lambda e: delete_account())
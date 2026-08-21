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
    login_window.geometry("400x400")
    login_window.configure(bg="#dff6f0")

    heading = Label(login_window,text="Login To Your Account",font=("Helvetica", 20, "bold"),bg="#dff6f0",fg="#002f34")
    heading.pack(pady=(20,25))

    Label(login_window,text="Email",font=("Helvetica", 12, "bold"),bg="#dff6f0").pack(pady=(0,5))
    saved_email=state.get_saved_user_email()
    email_entry=Entry(login_window,width=30)
    email_entry.pack(ipady=8,pady=(5,20))
    if saved_email :
        email_entry.insert(0,saved_email)

    Label(login_window,text="Password",font=("Helvetica", 12, "bold"),bg="#dff6f0").pack(pady=(0,5))
    password_entry = Entry(login_window,width=30,show="*")
    password_entry.pack(ipady=8,pady=(5,20))

    remember_var=BooleanVar(value=bool(saved_email))
    remember_check=Checkbutton(login_window,text="Remember Me",variable=remember_var,bg="#dff6f0",font=("Helvetica", 10))
    remember_check.pack(pady=(0,15))

    def login_user_gui():
        email = email_entry.get()
        password = password_entry.get()

        user = login_user(email, password)

        if user:
            state.current_user = user
            if remember_var.get() :
                state.save_user_email(email)
            else :
                state.save_user_email("")
            login_window.destroy()
            from dashboard_window import open_dashboard
            open_dashboard(window, user)
        else:
            messagebox.showerror("Error","Invalid Email or Password")

    login_btn = Label(login_window,text="Login",bg="#3a77ff",fg="white",font=("Helvetica", 13, "bold"),width=20,height=2,cursor="hand2")
    login_btn.pack(pady=(30,10))
    login_btn.bind("<Button-1>", lambda e: login_user_gui())


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
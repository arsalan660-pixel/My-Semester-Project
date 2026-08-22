from tkinter import Toplevel

def create_toplevel_window(parent, title, geometry):
    """Ek base window banata hai teal background ke sath taake code repeat na ho."""
    new_window = Toplevel(parent)
    new_window.title(title)
    new_window.geometry(geometry)
    new_window.configure(bg="#dff6f0")
    return new_window
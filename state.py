from collections import deque
from product import restore_products

current_user = None
recently_viewed = {}
deleted_products = {}


def get_saved_user_email():
    try:
        with open("database/saved_user.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""


def save_user_email(email):
    with open("database/saved_user.txt", "w") as file:
        file.write(email)


def track_view(product, user):
    if user[2] not in recently_viewed:
        recently_viewed[user[2]] = deque(maxlen=5)
    recently_viewed[user[2]].append(product)


def push_deleted(product, user):
    if user[2] not in deleted_products:
        deleted_products[user[2]] = []
    deleted_products[user[2]].append(product)


def undo_delete(user):
    email = user[2]
    if email not in deleted_products or not deleted_products[email]:
        return None
    product = deleted_products[email].pop()
    restore_products(*product.as_tuple())
    return product
import sqlite3

# Database connection
def connect():
    conn = sqlite3.connect("database/olx.db")
    return conn


# Add new product
def add_product(title, price, description, seller,image,category):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO products (title, price, description, seller,image,category)
    VALUES (?, ?, ?, ?,?,?)
    """, (title, price, description, seller,image,category))

    conn.commit()
    conn.close()


# Get all products
def get_products():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
 SELECT id, title, price, description, seller, image, status,category
 FROM products
 """)
    products = cursor.fetchall()

    conn.close()

    return products

def delete_product(product_id):

    conn = connect()

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM products WHERE id=?",
        (product_id,)
    )

    conn.commit()

    conn.close()
def mark_as_sold(product_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE products
        SET status = 'sold'
        WHERE id = ?
    """, (product_id,))

    conn.commit()
    conn.close()

from itertools import product
import sqlite3

# Database connection
def connect():
    conn = sqlite3.connect("database/olx.db")
    return conn


# Add new product
def add_product(title, price, description, seller,image,category,subcategory):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO products (title, price, description, seller,image,category,subcategory)
    VALUES (?, ?, ?, ?,?,?,?)
    """, (title, price, description, seller,image,category,subcategory))

    conn.commit()
    conn.close()

class Product:
    def __init__(self, row):
        self.id = row[0]
        self.title = row[1]
        self.price = row[2]
        self.description = row[3]
        self.seller = row[4]
        self.image = row[5]
        self.status = row[6] if row[6] else "available"
        self.category = row[7]
        self.subcategory = row[8]

    def as_tuple(self):
        return (self.id, self.title, self.price, self.description,
                self.seller, self.image, self.status, self.category, self.subcategory)



# Get all products
def get_products():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
 SELECT id, title, price, description, seller, image, status,category,subcategory
 FROM products
 """)
    rows = cursor.fetchall()

    conn.close()

    return [Product(row) for row in rows]

def restore_products(product_id,title,price,description,seller,image,status,category) :
    conn=connect()
    cursor=conn.cursor()
    cursor.execute("""
     INSERT INTO products (id,title,price,description,seller,image,status,category)
    VALUES(?,?,?,?,?,?,?,?) 
    """,(product_id,title,price,description,seller,image,status,category))
    conn.commit()
    conn.close()

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

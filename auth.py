import sqlite3
import bcrypt
import os

def connect():
    db_path = os.path.join(os.path.dirname(__file__), "database", "olx.db")
    conn = sqlite3.connect(db_path)
    return conn


def register_user(name, email, password):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?",(email,))
    existing_user=cursor.fetchone()
    if existing_user :
        conn.close()
        return False
    password_bytes=password.encode()
    salt=bcrypt.gensalt()
    hashed_password=bcrypt.hashpw(password_bytes,salt)
    hashed_password_str=hashed_password.decode()
    cursor.execute("""
    INSERT INTO users(name,email,password)
    VALUES (?,?,?)
    """,(name,email,hashed_password_str))
    conn.commit()
    conn.close()
    return True


def login_user(email, password):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?",(email,))
    user=cursor.fetchone()


    conn.close()
    if user is None :
        return None 
    stored_hash=user[3]
    password_matches=bcrypt.checkpw(password.encode(),stored_hash.encode())
    if password_matches :
        return user
    else :
        return None

def delete_user(email, password):

    conn = connect()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",(email,))
    user=cursor.fetchone()
    if user is None :
        conn.close()
        return False
    stored_hash=user[3]
    password_matches=bcrypt.checkpw(password.encode(),stored_hash.encode())

    if not password_matches :
        conn.close()
        return False
    cursor.execute("DELETE FROM users WHERE email=?",(email,))



    conn.commit()

    deleted = cursor.rowcount

    conn.close()

    return deleted


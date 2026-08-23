import sqlite3
import bcrypt
import os

def setup_admin_db():
    db_path = os.path.join(os.path.dirname(__file__), "database", "olx.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Check if 'role' column exists, if not, add it
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if "role" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
        print("✅ Role column added to users table.")
    else:
        print("ℹ️ Role column already exists.")

    # 2. Create a default Super Admin account
    admin_name = "Super Admin Arsalan"
    admin_email = "admin@olx.com"
    admin_password = "admin123" # Aap isay baad mein change kar sakte hain

    # Check if admin already exists
    cursor.execute("SELECT * FROM users WHERE email=?", (admin_email,))
    if cursor.fetchone():
        print("ℹ️ Admin account already exists.")
    else:
        # Hash the password
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(admin_password.encode(), salt).decode()
        
        # Insert admin
        cursor.execute("""
            INSERT INTO users(name, email, password, role)
            VALUES (?, ?, ?, ?)
        """, (admin_name, admin_email, hashed_pw, "admin"))
        print(f"✅ Admin account created successfully! \nEmail: {admin_email}\nPassword: {admin_password}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_admin_db()
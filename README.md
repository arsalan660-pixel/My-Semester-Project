# 🛒 OLX Desktop Clone (Modern Teal Edition)

A sleek, desktop based marketplace application developed using **Python**, **Tkinter**, and **SQLite**. This project allows users to securely register, manage their product listings, browse available items with advanced filtering, and make purchases through a clean, modern desktop interface.

## ✨ Key Features

**🔐 User & Security**
* Secure Registration & Login (Password Hashing via `bcrypt`)
* "Remember Me" functionality
* Account Deletion capabilities

**📦 Product Management**
* Sell Products with Image Upload support
* Dedicated "My Listings" view in a modern card-layout
* Delete and **Undo Delete** functionality
* Automatic "SOLD OUT" status updates
* Admin Panel And Product Management

**🔍 Discovery & Browsing**
* Dynamic Category and **Subcategory** filtering
* Title-based Search functionality
* Clean **Pagination** for browsing large inventories
* "Recently Viewed" history tracking

**🎨 UI/UX Enhancements**
* Modern **Teal Theme** (#00a49f & #002f34)
* Responsive Card-wrapper layouts for products and forms
* Hover effects and scrollable canvas areas
* Real-time Dashboard metrics (Active, Sold, Total Value)

## 🛠️ Technologies Used

* **Python 3.x**
* **Tkinter** (Standard GUI Library)
* **SQLite3** (Local Database)
* **Pillow (PIL)** (Image Processing)
* **bcrypt** (Password Security)

## 📂 Project Structure


MySemesterProject/
│
├── Gui.py                 # Main application entry point
├── auth.py                # Database auth logic
├── auth_windows.py        # Login, Register, Delete Account UI
├── dashboard_window.py    # User dashboard and metrics
├── product.py             # Product database operations
├── product_windows.py     # Product browsing, adding, and details UI
├── category_helpers.py    # Dynamic category tree logic
├── utils.py               # Shared UI helper functions
├── database/
│   └── olx.db             # SQLite database file
├── assets/                # Images and icons
├── requirements.txt       # Project dependencies
└── README.md
```

## 🚀 Installation & Setup

1. Clone or Download** the repository to your local machine.
2. Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   python Gui.py
   ```

## 👨‍💻 Team Members

Developed as a Semester Project for the **BS Information Technology** program at the **University of Management and Technology**.
* **Muhammad Arsalan**
* **Zeenat Imtiaz**

## 🔮 Future Improvements

* User Profile Management & Avatars
* Product Editing capabilities
* Wishlist / Favorites Feature
* Live Chat between Buyer and Seller
* Comprehensive Admin Panel

## 📄 License

This project was developed for educational purposes.

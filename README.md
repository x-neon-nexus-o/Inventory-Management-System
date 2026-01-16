# 🏪 Inventory Management System

[![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![MySQL](https://img.shields.io/badge/MySQL-Database-orange?style=for-the-badge&logo=mysql&logoColor=white)](https://mysql.com)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-GUI-green?style=for-the-badge)](https://github.com/TomSchimansky/CustomTkinter)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)

[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/x-neon-nexus-o/Inventory-Management-System)

A modern, feature-rich desktop application for inventory management built with Python and CustomTkinter. This system provides a complete solution for tracking products, managing orders, handling users, and analyzing sales data through an intuitive dark-themed GUI.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔐 **User Authentication** | Secure login, registration, and password reset |
| 👥 **Role-Based Access** | Separate views for ADMIN and USER (Biller) roles |
| 📊 **Interactive Dashboard** | Real-time metrics: sales, transactions, inventory count |
| 📦 **Inventory Control** | Add, delete, view products with auto-restock alerts |
| 🏷️ **Category Management** | GST/CGST/SGST tax rates per category |
| 🛒 **Order Management** | Create orders, track history, customer details |
| 📈 **Advanced Analytics** | Charts for trends, top products, revenue insights |
| 🧾 **PDF Invoices** | Auto-generate detailed invoices with tax breakdown |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.x** | Core backend logic |
| **CustomTkinter** | Modern dark-themed GUI |
| **MySQL** | Database storage |
| **Matplotlib** | Data visualization & charts |
| **ReportLab** | PDF invoice generation |
| **Pillow** | Image handling |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.x installed
- MySQL Server running

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/x-neon-nexus-o/inventory-management-system.git
cd inventory-management-system

# 2. Create virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install customtkinter mysql-connector-python matplotlib pillow reportlab

# 4. Run the application
python main.py
```

### ⚙️ Database Configuration

Update the MySQL credentials in `main.py` and `Analytics.py`:

```python
con = mycon.connect(host='localhost', user='root', passwd='YOUR_PASSWORD')
```

> 💡 The database and tables are created automatically on first run.

---

## 📖 Usage Guide

### Default Admin Account
| Username | Password |
|----------|----------|
| `ADMIN` | `ADMIN` |

### User Roles

| Role | Capabilities |
|------|-------------|
| **ADMIN** | Full inventory control, category management, view all orders, analytics dashboard |
| **USER (Biller)** | View inventory, create sales orders, view personal transaction history |

### Navigation
Use the left sidebar to switch between modules:
- 📊 **Dashboard** - Overview metrics and graphs
- 📦 **Inventory** - Product management
- 🛒 **Shop** - Create new orders (Biller)
- 📜 **History** - Transaction records
- 📈 **Analytics** - Advanced insights (Admin only)

---

## 📁 Project Structure

```
IMS/
├── main.py          # App entry point & database initialization
├── login.py         # Authentication GUI (login/register/reset)
├── menu.py          # Main application window & navigation
├── Analytics.py     # Analytics dashboard with charts
├── utils.py         # Helper functions & graph utilities
├── imgs/            # GUI icons and images
├── .venv/           # Virtual environment (not tracked)
└── Invoice_*.pdf    # Generated invoices (not tracked)
```

---

## 🔒 Security Features

- ✅ Parameterized SQL queries (SQL injection protection)
- ✅ Role-based access control
- ✅ Password masking in UI
- ✅ Sensitive data hidden for non-admin users

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Made with ❤️ using Python & CustomTkinter
</p>

# Inventory Management System
[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/x-neon-nexus-o/Inventory-Management-System)

An advanced desktop application for inventory management, built with Python. This system provides a comprehensive solution for tracking products, managing orders, handling users, and analyzing sales data through an intuitive graphical user interface.

## Key Features

- **User Authentication**: Secure login, registration, and password reset functionality.
- **Role-Based Access**: Differentiated views and permissions for 'ADMIN' and 'USER' (Biller) roles.
- **Interactive Dashboard**: At-a-glance view of key metrics like daily sales, total transactions, item counts, payment statuses, and monthly earnings.
- **Comprehensive Inventory Control**:
    - Add, delete, and view products.
    - Manage product categories with specific GST/CGST/SGST rates.
    - Automatic restocking notifications and updates when stock levels fall below a defined threshold.
- **Order Management**:
    - A dedicated shopping interface for billers to create new orders.
    - View detailed order history for both admins and users.
- **Advanced Analytics**: A separate analytics dashboard for admins to gain insights into:
    - Top-selling products
    - Revenue by product and category
    - Sales trends and location-based reports
    - Inventory distribution
- **Automated Invoicing**: Automatically generates and opens detailed PDF invoices for each transaction, including customer details and tax breakdowns (GST, CGST, SGST).
- **User Management**: Admins can view all registered users in the system.

## Technologies Used

- **Backend**: Python
- **GUI**: CustomTkinter
- **Database**: MySQL
- **Data Visualization**: Matplotlib
- **PDF Generation**: ReportLab
- **Image Handling**: Pillow (PIL)

## Setup and Installation

### Prerequisites

- Python 3.x
- A running MySQL Server instance.

### Steps

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/x-neon-nexus-o/inventory-management-system.git
    cd inventory-management-system
    ```

2.  **Install the required Python libraries:**
    ```sh
    pip install customtkinter mysql-connector-python matplotlib pillow reportlab
    ```

3.  **Configure the Database Connection:**
    - Open the `main.py` and `Analytics.py` files.
    - Locate the following line in both files:
      ```python
      con = mycon.connect(host='localhost', user='root', passwd='manager')
      ```
    - Update the `host`, `user`, and `passwd` parameters with your MySQL server credentials.

4.  **Run the Application:**
    - The application will automatically create the `inventory` database and the required tables on its first run.
    - Execute the `main.py` script to start the application.
    ```sh
    python main.py
    ```

## Usage

- **Default Admin Account**: On the first run, a default administrator account is created.
  - **Username**: `ADMIN`
  - **Password**: `ADMIN`
- **Login/Register**: Use the login screen to sign in or register a new 'USER' (biller) account.
- **Navigation**: Once logged in, use the left-side navigation panel to switch between different modules like Dashboard, Inventory, Orders, and Analytics (Admin only).
- **Admin Functions**: Admins can manage the full inventory, add new product categories, view all system-wide orders, and access the analytics dashboard.
- **User/Biller Functions**: Users can view the inventory, create new sales orders through the 'Shop' interface, and view their personal transaction history.

## File Structure

-   `main.py`: The entry point of the application. It handles database initialization and launches the login and menu windows.
-   `login.py`: Manages the user authentication GUI, including login, registration, and password reset functionalities.
-   `menu.py`: Contains the core logic for the main application window after login. It builds the navigation panel and all the different views (Dashboard, Inventory, Shop, etc.).
-   `Analytics.py`: Powers the standalone Analytics Dashboard, providing various charts and data visualizations for sales and inventory data.
-   `utils.py`: A utility module containing helper functions for creating error message boxes and generating graphs for the main dashboard.
-   `imgs/`: Directory containing images and icons used in the GUI.

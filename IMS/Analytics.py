import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector
from datetime import datetime

class Analytics:
    def __init__(self, con):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.con = con
        self.cur = con.cursor()

        self.window = ctk.CTk()
        self.window.title("Inventory Analytics Dashboard")
        self.window.geometry("1200x800")

        self.setup_ui()
        self.window.mainloop()

    def setup_ui(self):
        # Sidebar
        sidebar = ctk.CTkFrame(self.window, width=200, corner_radius=0)
        sidebar.pack(side="left", fill="y")

        # Sidebar buttons
        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Product Analytics", self.show_product_analytics),
            ("Category Insights", self.show_category_insights),
            ("Location Reports", self.show_location_reports),
            ("Trends", self.show_trends)
        ]
        for text, command in buttons:
            btn = ctk.CTkButton(sidebar, text=text, command=command, font=("Arial", 14))
            btn.pack(pady=10, padx=10, fill="x")

        # Main content area
        self.content_frame = ctk.CTkFrame(self.window)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Start with dashboard
        self.show_dashboard()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_content()
        title = ctk.CTkLabel(self.content_frame, text="Analytics Dashboard", font=("Arial", 24, "bold"))
        title.pack(pady=20)

        # Metrics frame
        metrics_frame = ctk.CTkFrame(self.content_frame)
        metrics_frame.pack(fill="x", pady=10)

        # Total sales
        sales_card = ctk.CTkFrame(metrics_frame, fg_color="#2a2d2e", corner_radius=10)
        sales_card.pack(side="left", padx=10, fill="x", expand=True)
        ctk.CTkLabel(sales_card, text="Total Sales", font=("Arial", 14)).pack(pady=5)
        total_sales = self.get_total_sales()
        ctk.CTkLabel(sales_card, text=f"Rs {total_sales:,.2f}", font=("Arial", 20, "bold")).pack()

        # Total products
        products_card = ctk.CTkFrame(metrics_frame, fg_color="#2a2d2e", corner_radius=10)
        products_card.pack(side="left", padx=10, fill="x", expand=True)
        ctk.CTkLabel(products_card, text="Total Products", font=("Arial", 14)).pack(pady=5)
        total_products = self.get_total_products()
        ctk.CTkLabel(products_card, text=total_products, font=("Arial", 20, "bold")).pack()

        # Charts frame
        charts_frame = ctk.CTkFrame(self.content_frame)
        charts_frame.pack(fill="both", expand=True, pady=20)

        # Top products chart
        top_products_frame = ctk.CTkFrame(charts_frame)
        top_products_frame.pack(side="left", padx=10, fill="both", expand=True)
        self.create_top_products_chart(top_products_frame, "Top 5 Products")

        # Category revenue chart
        category_frame = ctk.CTkFrame(charts_frame)
        category_frame.pack(side="left", padx=10, fill="both", expand=True)
        self.create_category_revenue_chart(category_frame, "Category Revenue")

    def show_product_analytics(self):
        self.clear_content()
        title = ctk.CTkLabel(self.content_frame, text="Product Analytics", font=("Arial", 24, "bold"))
        title.pack(pady=20)

        charts_frame = ctk.CTkFrame(self.content_frame)
        charts_frame.pack(fill="both", expand=True, pady=20)

        # Top 5 best-selling
        top_frame = ctk.CTkFrame(charts_frame)
        top_frame.pack(side="left", padx=10, fill="both", expand=True)
        self.create_top_products_chart(top_frame, "Top 5 Best-Selling Products")

        # Revenue per product
        revenue_frame = ctk.CTkFrame(charts_frame)
        revenue_frame.pack(side="left", padx=10, fill="both", expand=True)
        self.create_revenue_per_product_chart(revenue_frame)

        # Least-selling products
        least_frame = ctk.CTkFrame(self.content_frame)
        least_frame.pack(fill="x", pady=20)
        self.create_least_selling_products(least_frame)

    def show_category_insights(self):
        self.clear_content()
        title = ctk.CTkLabel(self.content_frame, text="Category Insights", font=("Arial", 24, "bold"))
        title.pack(pady=20)

        charts_frame = ctk.CTkFrame(self.content_frame)
        charts_frame.pack(fill="both", expand=True, pady=20)

        # Category revenue chart
        revenue_frame = ctk.CTkFrame(charts_frame)
        revenue_frame.pack(side="left", padx=10, fill="both", expand=True)
        self.create_category_revenue_chart(revenue_frame, "Revenue by Category")

        # Products per category chart
        products_frame = ctk.CTkFrame(charts_frame)
        products_frame.pack(side="left", padx=10, fill="both", expand=True)
        self.create_products_per_category_chart(products_frame)

    def show_location_reports(self):
        self.clear_content()
        title = ctk.CTkLabel(self.content_frame, text="Location Reports", font=("Arial", 24, "bold"))
        title.pack(pady=20)

        charts_frame = ctk.CTkFrame(self.content_frame)
        charts_frame.pack(fill="both", expand=True, pady=20)

        # Location sales chart
        sales_frame = ctk.CTkFrame(charts_frame)
        sales_frame.pack(side="left", padx=10, fill="both", expand=True)
        self.create_location_sales_chart(sales_frame)

        # Inventory distribution chart
        inventory_frame = ctk.CTkFrame(charts_frame)
        inventory_frame.pack(side="left", padx=10, fill="both", expand=True)
        self.create_inventory_distribution_chart(inventory_frame)

    def show_trends(self):
        self.clear_content()
        title = ctk.CTkLabel(self.content_frame, text="Trend Analysis", font=("Arial", 24, "bold"))
        title.pack(pady=20)

        trends_frame = ctk.CTkFrame(self.content_frame)
        trends_frame.pack(fill="both", expand=True, pady=20)
        self.create_monthly_trends_chart(trends_frame)

    # Visualization methods
    def create_top_products_chart(self, parent, title="Top Products"):
        query = """
            SELECT p.product_name, SUM(oi.quantity) AS total_sold
            FROM order_items oi JOIN products p ON oi.product_id = p.product_id
            GROUP BY oi.product_id ORDER BY total_sold DESC LIMIT 5;
        """
        self.cur.execute(query)
        data = self.cur.fetchall()
        fig, ax = plt.subplots(figsize=(6, 4))
        names, quantities = zip(*data) if data else ([], [])
        ax.barh(names, quantities, color='skyblue')
        ax.set_title(title)
        ax.set_xlabel('Quantity Sold')
        ax.invert_yaxis()
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_revenue_per_product_chart(self, parent):
        query = """
            SELECT p.product_name, SUM(oi.quantity * oi.price) AS revenue
            FROM order_items oi JOIN products p ON oi.product_id = p.product_id
            GROUP BY oi.product_id ORDER BY revenue DESC LIMIT 10;
        """
        self.cur.execute(query)
        data = self.cur.fetchall()
        fig, ax = plt.subplots(figsize=(6, 4))
        names, revenues = zip(*data) if data else ([], [])
        ax.barh(names, revenues, color='lightgreen')
        ax.set_title("Revenue by Product")
        ax.set_xlabel('Revenue (Rs)')
        ax.invert_yaxis()
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_category_revenue_chart(self, parent, title="Category Revenue"):
        query = """
            SELECT p.category, SUM(oi.quantity * oi.price) AS revenue
            FROM order_items oi JOIN products p ON oi.product_id = p.product_id
            GROUP BY p.category;
        """
        self.cur.execute(query)
        data = self.cur.fetchall()
        fig, ax = plt.subplots(figsize=(6, 4))
        categories, revenues = zip(*data) if data else ([], [])
        ax.pie(revenues, labels=categories, autopct='%1.1f%%', startangle=90)
        ax.set_title(title)
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_products_per_category_chart(self, parent):
        query = "SELECT category, COUNT(*) AS count FROM products GROUP BY category;"
        self.cur.execute(query)
        data = self.cur.fetchall()
        fig, ax = plt.subplots(figsize=(6, 4))
        categories, counts = zip(*data) if data else ([], [])
        ax.bar(categories, counts, color='orange')
        ax.set_title("Products per Category")
        ax.set_xlabel('Category')
        ax.set_ylabel('Count')
        plt.xticks(rotation=45)
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_location_sales_chart(self, parent):
        query = """
            SELECT SUBSTRING(address, 1, 10) AS location, SUM(total_amount) AS revenue
            FROM orders GROUP BY address;
        """
        self.cur.execute(query)
        data = self.cur.fetchall()
        fig, ax = plt.subplots(figsize=(6, 4))
        locations, revenues = zip(*data) if data else ([], [])
        ax.pie(revenues, labels=locations, autopct='%1.1f%%', startangle=90)
        ax.set_title("Sales by Location")
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_inventory_distribution_chart(self, parent):
        query = """
            SELECT SUBSTRING(o.address, 1, 10), SUM(p.quantity) 
            FROM products p 
            JOIN order_items oi ON p.product_id = oi.product_id 
            JOIN orders o ON oi.order_id = o.order_id 
            WHERE o.address IS NOT NULL  -- Filter out NULL addresses
            GROUP BY o.address;
        """
        self.cur.execute(query)
        data = self.cur.fetchall()
        fig, ax = plt.subplots(figsize=(6, 4))

        # Filter out any rows where address or quantity is None
        valid_data = [(loc, qty) for loc, qty in data if loc is not None and qty is not None]
        locations, quantities = zip(*valid_data) if valid_data else ([], [])

        ax.bar(locations, quantities, color='gold')
        ax.set_title("Inventory by Location")
        ax.set_xlabel('Location')
        ax.set_ylabel('Quantity')
        plt.xticks(rotation=45)
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_monthly_trends_chart(self, parent):
        query = """
            SELECT MONTH(o.date), SUM(oi.quantity * oi.price) 
            FROM orders o JOIN order_items oi ON o.order_id = oi.order_id 
            WHERE YEAR(o.date) = YEAR(CURDATE()) GROUP BY MONTH(o.date) ORDER BY MONTH(o.date);
        """
        self.cur.execute(query)
        data = self.cur.fetchall()
        fig, ax = plt.subplots(figsize=(10, 5))
        months, revenues = zip(*data) if data else (range(1, 13), [0]*12)
        ax.plot(months, revenues, marker='o', color='purple')
        ax.set_title("Monthly Revenue Trends")
        ax.set_xlabel('Month')
        ax.set_ylabel('Revenue (Rs)')
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_least_selling_products(self, parent):
        query = """
            SELECT p.product_name, SUM(oi.quantity) AS total_sold
            FROM products p LEFT JOIN order_items oi ON p.product_id = oi.product_id
            GROUP BY p.product_id ORDER BY total_sold ASC LIMIT 5;
        """
        self.cur.execute(query)
        data = self.cur.fetchall()
        frame = ctk.CTkFrame(parent, fg_color="#2a2d2e")
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(frame, text="Least Selling Products", font=("Arial", 18, "bold")).pack(pady=10)
        if data:
            table = ctk.CTkFrame(frame)
            table.pack(fill="both", expand=True)
            ctk.CTkLabel(table, text="Product", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=5)
            ctk.CTkLabel(table, text="Sold", font=("Arial", 14, "bold")).grid(row=0, column=1, padx=10, pady=5)
            for i, (name, sold) in enumerate(data):
                ctk.CTkLabel(table, text=name).grid(row=i+1, column=0, padx=10, pady=5)
                ctk.CTkLabel(table, text=sold if sold else 0).grid(row=i+1, column=1, padx=10, pady=5)
        else:
            ctk.CTkLabel(frame, text="No data available").pack(pady=20)

    def get_total_sales(self):
        self.cur.execute("SELECT SUM(total_amount) FROM orders")
        result = self.cur.fetchone()[0]
        return result if result else 0

    def get_total_products(self):
        self.cur.execute("SELECT COUNT(*) FROM products")
        return self.cur.fetchone()[0]

if __name__ == "__main__":
    con = mysql.connector.connect(host='localhost', user='root', password='manager', database='inventory')
    if con.is_connected():
        print("Connected to database")
        analytics = Analytics(con)
    else:
        print("Failed to connect to database")
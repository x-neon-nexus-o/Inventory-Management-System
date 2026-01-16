import tkinter
from tkinter import ttk, messagebox
from datetime import date
import customtkinter as ctk
from PIL import Image
from Analytics import Analytics

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from datetime import datetime
import io

from utils import error, add_graphs


class Menu():
    """Represents a menu for the inventory management system."""

    def __init__(self, con, user, login_win):
        # Set window theme as dark
        ctk.set_default_color_theme("dark-blue")
        ctk.set_appearance_mode("dark")
        # ctk.deactivate_automatic_dpi_awareness()
        self.login_win = login_win
        self.window = ctk.CTkToplevel(self.login_win)
        self.window.protocol("WM_DELETE_WINDOW", exit)
        self.con = con
        self.cur = con.cursor()
        self.user = user
        self.font = 'Century Gothic'
        self._logged_out = False
        self.make_window()

    def make_window(self):
        """ Create a window to display a menu"""
        width = 1350
        height = 740
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.window.geometry("%dx%d+%d+%d" % (width, height, x, y))
        self.login_win.withdraw()
        self.make_panel()

    def show_analytics(self):
        from Analytics import Analytics
        analytics = Analytics(self.con)
        analytics.window.mainloop()

    def make_panel(self):
        """ Create side panel or navigation panel"""
        side_panel = ctk.CTkFrame(self.window, corner_radius=0, width=250)
        side_panel.pack(fill="y", side="left")

        section_functions = {
            "dashboard": self.dashboard,
            "inventory": self.inventory,
            "orders": self.orders,
            "users": self.users,
            "analytics": self.show_analytics,
            "shop": self.shop,
            "history": self.history,
            "logout": self.logout
        }

        # Added buttons for different sections in the side panel
        if self.user[2] == 'ADMIN':
            sections = ["dashboard", "inventory", "orders", "users", "logout"]
        else:
            sections = ["dashboard", "inventory", "shop", "history", "logout"]

        for section in sections:
            img = ctk.CTkImage(Image.open(f"./imgs/{section}.png").resize((30, 30)), size=(30, 30))
            button = ctk.CTkButton(side_panel, text=section.title(), image=img, anchor="w", font=(self.font, 18),
                                   fg_color="transparent", hover_color="#212121", command=section_functions[section])
            button.pack(padx=50, pady=50)

        self.frame = ctk.CTkFrame(self.window, corner_radius=0, fg_color="#1a1a1a")
        self.frame.pack(fill="both", expand=True)
        self.dashboard()

    def set_title(self, title):
        """
        Sets the title of the user interface window.
        Args:
            title (str): The title to set for the window.
        """
        try:
            self.frame.forget()
            self.frame = ctk.CTkFrame(self.window, corner_radius=0, fg_color="#1a1a1a")
            self.frame.pack(fill="both", expand=True)

        except:
            pass
        self.window.title(title)
        heading = ctk.CTkLabel(self.frame, text=title, anchor="center", font=(self.font, 33))
        heading.pack()

    def dashboard(self):
        """ Displays the dashboard section of the user interface."""
        self.set_title("Dashboard")

        # Create a frame for the statistics cards
        stats_frame = ctk.CTkFrame(master=self.frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=20)

        x = 50
        self.cur.execute("SELECT COUNT(*) FROM orders WHERE Date(date) = Curdate();")
        sales = self.cur.fetchall()[0]
        self.cur.execute("SELECT COUNT(*) FROM orders;")
        transactions = self.cur.fetchall()[0]
        self.cur.execute("SELECT COUNT(*) FROM products;")
        items = self.cur.fetchall()[0]

        header = {"Total Sales Today": sales, "Total Transactions": transactions, "Items in Inventory": items}
        for title in header:
            card = ctk.CTkFrame(master=stats_frame, width=300, height=150, corner_radius=15, fg_color="#007fff")
            card.pack(side="left", padx=10)

            value_label = ctk.CTkLabel(card, text=header[title], fg_color="#007fff", font=(self.font, 30))
            value_label.place(relx=0.5, rely=0.4, anchor="center")

            title_label = ctk.CTkLabel(card, text=title, fg_color="#007fff", font=(self.font, 16))
            title_label.place(relx=0.5, rely=0.7, anchor="center")

        # Analytics button (only for admin)
        if self.user[2] == 'ADMIN':
            # Create a frame to hold the analytics button
            analytics_frame = ctk.CTkFrame(master=self.frame, fg_color="transparent")
            analytics_frame.pack(fill="x", padx=20, pady=20)

            # Place the analytics button in the center of the frame
            analytics_button = ctk.CTkButton(
                analytics_frame,
                text="View Analytics",
                command=self.show_analytics,
                fg_color="#00cc00",
                font=(self.font, 20),
                width=200  # Adjust width to ensure it fits
            )
            analytics_button.pack(pady=10)  # Add padding to ensure it doesn't get cut-off # Place below the cards and center it

        # Create a frame for the graphs
        graphs_frame = ctk.CTkFrame(master=self.frame, fg_color="transparent")
        graphs_frame.pack(fill="both", expand=True, padx=20, pady=20)

        try:
            add_graphs(self.cur, graphs_frame)
        except Exception as e:
            print(f"Error adding graphs: {e}")
            error("Failed to load dashboard graphs")

    # In menu.py, modify the inventory method to include the "Add Category" button
    def inventory(self):
        """ Displays the inventory section of the user interface. """
        self.set_title("Inventory")
        if self.user[2] == 'ADMIN':
            add_button = ctk.CTkButton(self.frame, width=100, command=self.add_button, text="Add Item",
                                       fg_color="#007fff", font=(self.font, 20))
            add_button.place(x=50, y=50)

            delete_button = ctk.CTkButton(self.frame, width=100, command=self.delete_product, text="Delete Item",
                                          fg_color="#fb0000", font=(self.font, 20))
            delete_button.place(x=170, y=50)

            # Add Category button
            add_category_button = ctk.CTkButton(self.frame, width=100, command=self.add_category_form,
                                                text="Add Category",
                                                fg_color="#00cc00", font=(self.font, 20))
            add_category_button.place(x=300, y=50)

        self.make_table(("Product ID", "Product Name", "Description", "Price", "Quantity", "Category"), 130, "products")

    # New method to create the Add Category form
    def add_category_form(self):
        """Creates a new window with entry fields to add a category to the inventory."""
        self.category_win = ctk.CTkToplevel(self.window)
        self.category_win.title("Add New Category")
        self.category_win.geometry("500x400")

        frame = ctk.CTkFrame(master=self.category_win, width=450, height=370, corner_radius=15)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Category Name Entry
        category_label = ctk.CTkLabel(frame, text="Category Name", font=(self.font, 14))
        category_label.pack(pady=(10, 0))
        self.category_name_entry = ctk.CTkEntry(master=frame, placeholder_text="Enter category name", width=350,
                                                height=35)
        self.category_name_entry.pack(pady=(0, 10))

        # GST Percentage Entry
        gst_label = ctk.CTkLabel(frame, text="GST Percentage (%)", font=(self.font, 14))
        gst_label.pack(pady=(10, 0))
        self.gst_entry = ctk.CTkEntry(master=frame, placeholder_text="Enter GST percentage (e.g., 18)", width=350,
                                      height=35)
        self.gst_entry.pack(pady=(0, 10))

        # CGST and SGST Display Labels (read-only)
        cgst_label = ctk.CTkLabel(frame, text="CGST (%)", font=(self.font, 14))
        cgst_label.pack(pady=(10, 0))
        self.cgst_value = ctk.CTkLabel(frame, text="0.00", font=(self.font, 14))
        self.cgst_value.pack(pady=(0, 10))

        sgst_label = ctk.CTkLabel(frame, text="SGST (%)", font=(self.font, 14))
        sgst_label.pack(pady=(10, 0))
        self.sgst_value = ctk.CTkLabel(frame, text="0.00", font=(self.font, 14))
        self.sgst_value.pack(pady=(0, 10))

        # Bind GST entry to update CGST and SGST dynamically
        self.gst_entry.bind("<KeyRelease>", self.update_tax_values)

        # Add Category Button
        add_button = ctk.CTkButton(master=frame, width=400, text="Add Category", corner_radius=6,
                                   command=self.add_category)
        add_button.pack(pady=20)

    def update_tax_values(self, event=None):
        """Dynamically updates CGST and SGST values based on GST input."""
        try:
            gst = float(self.gst_entry.get())
            cgst = gst / 2
            sgst = gst / 2
            self.cgst_value.configure(text=f"{cgst:.2f}")
            self.sgst_value.configure(text=f"{sgst:.2f}")
        except ValueError:
            self.cgst_value.configure(text="0.00")
            self.sgst_value.configure(text="0.00")

    def add_category(self):
        """Adds a new category to the category table with GST, CGST, and SGST values."""
        category_name = self.category_name_entry.get().strip()
        gst_str = self.gst_entry.get().strip()

        # Validation
        if not category_name:
            error("Category name cannot be empty")
            return
        if len(category_name) > 50:
            error("Category name must be less than 50 characters")
            return

        try:
            gst = float(gst_str)
            if gst < 0 or gst > 100:
                error("GST percentage must be between 0 and 100")
                return
        except ValueError:
            error("GST must be a valid number")
            return

        # Calculate CGST and SGST
        cgst = gst / 2
        sgst = gst / 2

        # Check for duplicate category
        self.cur.execute("SELECT * FROM categories WHERE category_name = %s", (category_name,))
        if self.cur.fetchall():
            error("Category already exists")
            return

        # Insert into database
        try:
            self.cur.execute(
                "INSERT INTO categories (category_name, GST, SGST, CGST) VALUES (%s, %s, %s, %s)",
                (category_name, gst, sgst, cgst)
            )
            self.con.commit()
            messagebox.showinfo("Success", f"Category '{category_name}' added successfully!")
            self.category_win.destroy()
            self.inventory()  # Refresh the inventory view
        except Exception as e:
            error(f"Failed to add category: {str(e)}")

    def make_table(self, col, width, table=None, height=600):
        """Create a tkinter treeview table with specified columns, column widths, and optional data source table."""
        tableframe = ctk.CTkScrollableFrame(self.frame, width=1000, height=height)
        tableframe.place(x=1070, y=100, anchor=tkinter.NE)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#007fff')])

        style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat")
        style.map("Treeview.Heading",
                  background=[('active', '#3484F0')])
        self.tree = ttk.Treeview(tableframe, columns=col,
                                 selectmode="browse", height=100)

        for i, value in enumerate(col):
            if value == 'Price':
                w = 300
            else:
                w = 0 if i == 0 else width
            self.tree.column(f'#{i}', stretch=tkinter.NO, minwidth=30, width=w)
            self.tree.heading(value, text=value, anchor=tkinter.W)

        self.tree.grid(row=1, column=0, sticky="W")
        self.tree.pack(fill="both", expand=True)
        if table:
            self.render_table(table)

    def users(self):
        """ Displays the Users section of the user interface. """
        self.set_title("Users")
        self.make_table(("Username", "Password", "Account Type", "Email"), 170, "users")

    def shop(self):
        """ Displays the shop section of the user interface. """
        self.set_title("Shop Items")
        add_button = ctk.CTkButton(self.frame, width=50, command=self.add_item, text="Add Item",
                                   fg_color="#007fff", font=(self.font, 25))
        add_button.place(x=50, y=50)

        remove_button = ctk.CTkButton(self.frame, width=50, command=self.remove_item, text="Remove Item",
                                      fg_color="#fb0000", font=(self.font, 25))
        remove_button.place(x=50, y=580)  # Adjusted y position to place the button below the table

        label = ctk.CTkLabel(self.frame, text="Total Amount :", font=(self.font, 30))
        label.place(x=700, y=530)

        button = ctk.CTkButton(master=self.frame, width=390, text="Sell Items", corner_radius=6, command=self.buy)
        button.place(x=700, y=600)
        headings = ("Product Id", "Product Name", "Description", "Price", "Quantity", "Total Amount", "Customer Name",
                    "Phone Number", "Address")
        self.make_table(headings, 130, height=400)

    def orders(self):
        """ Displays all the Orders placed in the system."""
        self.set_title("Orders")
        headings = (
        "Order Id", "User", "Date", "Total Items", "Total Amount", "Payment Status", "Customer Name", "Phone Number",
        "Address")
        self.make_table(headings, 130, "orders")

    def history(self):
        """ Displays the order history of the user. """
        self.set_title("Transactions History")
        headings = ("Order Id", "Product Name", "Quantity", "Price", "Date", "Payment Status", "Customer Name")
        query = '''SELECT o.order_id , p.product_name, oi.quantity , oi.price , o.date, o.payment_status, o.customer_name
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        WHERE o.user = %s;
        '''
        self.make_table(headings, 130)
        self.cur.execute(query, (self.user[0],))
        items = self.cur.fetchall()
        for item in items:
            self.tree.insert('', 'end', values=item)

    def add_item(self):
        """Display another window to add items to cart"""
        new_win = ctk.CTkToplevel(self.window)
        new_win.title("Add item to Cart")
        new_win.geometry("500x700")

        self.win_frame = ctk.CTkFrame(master=new_win, width=480, height=670, corner_radius=15)
        self.win_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # Category combobox
        label = ctk.CTkLabel(self.win_frame, text="Select Category:", font=(self.font, 20))
        label.place(x=50, y=50)

        # Fetch categories from the database
        self.cur.execute("SELECT category_name FROM categories")
        categories = self.cur.fetchall()
        category_names = [category[0] for category in categories]

        self.category_var = ctk.StringVar(value="")
        self.category_combobox = ctk.CTkComboBox(
            self.win_frame,
            values=category_names,
            variable=self.category_var,
            width=200,
            command=self.update_products
        )
        self.category_combobox.place(x=250, y=50)

        # Product combobox
        self.product_label = ctk.CTkLabel(self.win_frame, text="Select Product:", font=(self.font, 20))
        self.product_label.place(x=50, y=100)

        self.product_var = ctk.StringVar(value="")
        self.product_combobox = ctk.CTkComboBox(
            self.win_frame,
            values=[],
            variable=self.product_var,
            width=200,
            state="readonly",
            command=self.fill_product_details
        )
        self.product_combobox.place(x=250, y=100)

        # Labels for product details
        self.available_quantity_label = ctk.CTkLabel(self.win_frame, text="Available Quantity:", font=(self.font, 20))
        self.available_quantity_label.place(x=50, y=150)
        self.available_quantity_value = ctk.CTkLabel(self.win_frame, text="", font=(self.font, 20))
        self.available_quantity_value.place(x=250, y=150)

        self.unit_price_label = ctk.CTkLabel(self.win_frame, text="Unit Price:", font=(self.font, 20))
        self.unit_price_label.place(x=50, y=200)
        self.unit_price_value = ctk.CTkLabel(self.win_frame, text="", font=(self.font, 20))
        self.unit_price_value.place(x=250, y=200)

        # Quantity spinbox (placed in front of the label)
        self.quantity_label = ctk.CTkLabel(self.win_frame, text="Quantity:", font=(self.font, 20))
        self.quantity_label.place(x=50, y=250)

        style = ttk.Style()
        style.configure("TSpinbox", arrowsize=20, fieldbackground="#343638", foreground="white", background="#343638")
        self.quantity_spinbox = ttk.Spinbox(
            self.win_frame,
            from_=1,
            to=1,
            width=10,
            font=(self.font, 20),
            style="TSpinbox"
        )
        self.quantity_spinbox.place(x=250, y=383)  # Positioned to the right of the label

        # Customer name entry
        self.customer_name_label = ctk.CTkLabel(self.win_frame, text="Customer Name:", font=(self.font, 20))
        self.customer_name_label.place(x=50, y=300)
        self.customer_name_entry = ctk.CTkEntry(self.win_frame, width=200)
        self.customer_name_entry.place(x=250, y=300)

        self.phone_number_label = ctk.CTkLabel(self.win_frame, text="Phone Number:", font=(self.font, 20))
        self.phone_number_label.place(x=50, y=350)
        self.phone_number_entry = ctk.CTkEntry(self.win_frame, width=200)
        self.phone_number_entry.place(x=250, y=350)

        self.address_label = ctk.CTkLabel(self.win_frame, text="Address:", font=(self.font, 20))
        self.address_label.place(x=50, y=400)
        self.address_entry = ctk.CTkEntry(self.win_frame, width=200)
        self.address_entry.place(x=250, y=400)

        # Add button
        button = ctk.CTkButton(master=self.win_frame, width=400, text="Add", corner_radius=6, command=self.add_to_cart)
        button.place(x=25, y=460)

    def update_products(self, choice):
        """Update the product combobox based on the selected category."""
        category = self.category_var.get()
        if not category:
            self.product_combobox.configure(values=[])
            return

        # Fetch products for the selected category
        self.cur.execute("SELECT product_name FROM products WHERE category = %s", (category,))
        products = self.cur.fetchall()
        product_names = [product[0] for product in products]

        # Update the product combobox
        self.product_combobox.configure(values=product_names)
        self.product_combobox.set("")  # Clear the selection

    def fill_product_details(self, choice):
        """Fill product details (available quantity and unit price) when a product is selected."""
        product_name = self.product_var.get()
        if not product_name:
            self.available_quantity_value.configure(text="")
            self.unit_price_value.configure(text="")
            return

        # Fetch product details
        self.cur.execute("SELECT quantity, price FROM products WHERE product_name = %s", (product_name,))
        fetch = self.cur.fetchone()
        if not fetch:
            error("Product details not found")
            return

        quantity, price = fetch
        self.available_quantity_value.configure(text=str(quantity))
        self.unit_price_value.configure(text=str(price))
        self.quantity_spinbox.configure(to=quantity)

    def remove_item(self):
        """ Removes selected item from the cart."""
        selected_item = self.tree.selection()

        if selected_item and messagebox.askyesno('Alert!', 'Do you want to remove this item?') == True:
            for i in selected_item:
                item = self.tree.item(i)
                self.tree.delete(i)

                values = item['values']

            p_id = values[0]
            qty = values[4]
            self.cur.execute("UPDATE products SET quantity = quantity + %s WHERE product_id = %s", (qty, p_id))
            self.con.commit()
        self.total()

    def fill_labels(self, choice):
        """Fills labels with data of a particular item chosen by user"""
        product_name = self.product_var.get()
        if not product_name:
            error("Please select a product")
            return

        self.cur.execute("SELECT quantity, price FROM products WHERE product_name = %s", (product_name,))
        fetch = self.cur.fetchall()
        if not fetch:
            error("Product not found")
            return

        quantity, price = fetch[0]
        self.spin_var = ctk.IntVar(value=1)
        x = 250

        try:
            self.quantity_label.place_forget()
            self.price_label.place_forget()
            self.spinbox.place_forget()
            self.customer_name_entry.place_forget()
        except:
            pass

        self.quantity_label = ctk.CTkLabel(self.win_frame, text=quantity, font=(self.font, 20))
        self.quantity_label.place(x=x, y=150)
        self.price_label = ctk.CTkLabel(self.win_frame, text=price, font=(self.font, 20))
        self.price_label.place(x=x, y=210)

        style = ttk.Style()
        style.configure("TSpinbox", fieldbackground="#343638", foreground="white", background="#343638")

        self.spinbox = ttk.Spinbox(
            self.win_frame,
            from_=1,
            to=quantity,
            textvariable=self.spin_var,
            style="TSpinbox",
            width=20
        )
        self.spinbox.place(x=250, y=330)

        # Add customer name entry field
        self.customer_name_entry = ctk.CTkEntry(
            self.win_frame,
            placeholder_text="Customer Name",
            width=200
        )
        self.customer_name_entry.place(x=250, y=270)

    def add_to_cart(self):
        """Add the selected product to the cart with the specified quantity."""
        product_name = self.product_var.get()
        if not product_name:
            error("Please select a product")
            return

        try:
            quantity = int(self.quantity_spinbox.get())
            if quantity <= 0:
                error("Please enter a valid quantity")
                return

            customer_name = self.customer_name_entry.get()
            phone_number = self.phone_number_entry.get()  # Get phone number
            address = self.address_entry.get()  # Get address

            if not customer_name or not phone_number or not address:
                error("Please fill all fields: Customer Name, Phone Number, Address")
                return

            # Fetch product details
            self.cur.execute("SELECT product_id, description, price FROM products WHERE product_name = %s", (product_name,))
            product = self.cur.fetchone()
            if not product:
                error("Product not found")
                return

            p_id, desc, price = product
            total = price * quantity

            # Insert into the cart (assuming self.tree is the Treeview for the cart)
            self.tree.insert('', 'end', values=(
                p_id, product_name, desc, price, quantity, total, customer_name, phone_number, address
            ))

            # Update the total amount displayed
            self.total()

        except Exception as e:
            error(f"Error adding item to cart: {str(e)}")

    def total(self):
        """Evaluates the total amount in cart and displays it"""
        total = round(sum(float(self.tree.item(item, "values")[-2]) for item in self.tree.get_children()), 2)
        try:
            self.total_label.place_forget()
        except:
            pass
        self.total_label = ctk.CTkLabel(self.frame, text=total, font=(self.font, 22))
        self.total_label.place(x=940, y=538)

    # menu.py
    def add_button(self):
        """Creates a new window with entry fields to add a product to the inventory."""
        self.topwin = ctk.CTkToplevel(self.window)
        self.topwin.title("Add item to Inventory")
        self.topwin.geometry("500x700")
        frame = ctk.CTkFrame(master=self.topwin, width=450, height=670, corner_radius=15)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.product_entries = {}
        items = ['Product Id', 'Product Name', 'Description', 'Price', 'Quantity', 'Category', 'Restock Level',
                 'Restock Quantity']

        for i in items:
            label = ctk.CTkLabel(frame, text=i, font=(self.font, 14))
            label.pack(pady=(10, 0))
            if i == 'Category':
                # Fetch categories from the database
                self.cur.execute("SELECT category_name FROM categories")
                categories = self.cur.fetchall()
                category_names = [category[0] for category in categories]

                # Create a combobox for categories
                self.category_var = ctk.StringVar(value="")
                combobox = ctk.CTkComboBox(frame, values=category_names, variable=self.category_var, width=350)
                combobox.pack(pady=(0, 10))
                self.product_entries[i] = combobox
            else:
                entry = ctk.CTkEntry(master=frame, placeholder_text=i, width=350, height=35)
                entry.pack(pady=(0, 10))
                self.product_entries[i] = entry

        # Place the "Add" button below the entry fields
        button = ctk.CTkButton(master=frame, width=400, text="Add", corner_radius=6, command=self.add_product)
        button.pack(pady=20)

    def buy(self):
        """Function to buy items which are added to cart"""
        all_items = self.tree.get_children()
        if not all_items:
            error("No items available. Add items to cart to buy")
            return

        result = messagebox.askquestion("Payment", "Pay Now ?")
        if result == "yes":
            payment_status = "paid"
        else:
            payment_status = "pending"

        # Fetch the next order_id
        self.cur.execute("SELECT MAX(order_id) FROM orders")
        max_order_id = self.cur.fetchone()[0]
        order_id = max_order_id + 1 if max_order_id else 1001  # Start from 1001 if no orders exist

        # Fetch the next order_item_id
        self.cur.execute("SELECT MAX(order_item_id) FROM order_items")
        max_order_item_id = self.cur.fetchone()[0]
        order_item_id = max_order_item_id + 1 if max_order_item_id else 1

        items = []
        customer_name = None
        phone_number = None
        address = None

        for item in all_items:
            values = self.tree.item(item, "values")
            product_id = values[0]
            quantity = values[4]  # Assuming quantity is at index 4
            price = values[3]  # Assuming price is at index 3
            customer_name = values[6]  # Assuming customer name is at index 6
            phone_number = values[7]  # Assuming phone number is at index 7
            address = values[8]  # Assuming address is at index 8
            items.append(values)

            # Deduct the quantity from the product inventory using a parameterized query
            self.cur.execute(
                "UPDATE products SET quantity = quantity - %s WHERE product_id = %s",
                (quantity, product_id)
            )

            # Add to order_items using a parameterized query
            self.cur.execute(
                "INSERT INTO order_items (order_item_id, order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s, %s)",
                (order_item_id, order_id, product_id, quantity, price)
            )
            order_item_id += 1

        total_amount = sum(
            float(self.tree.item(item, "values")[5]) for item in all_items)  # Assuming total is at index 5
        total_items = len(all_items)

        # Insert into order table using a parameterized query
        self.cur.execute(
            "INSERT INTO orders (order_id, user, date, total_items, total_amount, payment_status, customer_name, phone_number, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (order_id, self.user[0], date.today(), total_items, total_amount, payment_status, customer_name,
             phone_number, address)
        )

        self.con.commit()

        # Generate invoice
        self.generate_invoice(order_id, customer_name, items, total_amount, phone_number, address)

        # Check if any product needs restocking
        self.check_and_restock_products()

        messagebox.showinfo("Success", "Order placed successfully.")
        self.tree.delete(*self.tree.get_children())
        self.render_table("products")  # Refresh the product table

    def check_and_restock_products(self):
        """Checks if any products need restocking and restocks them if necessary."""
        self.cur.execute("SELECT product_id, quantity, restock_level, restock_quantity FROM products")
        products = self.cur.fetchall()
        restocked_products = []

        for product in products:
            product_id, current_quantity, restock_level, restock_quantity = product
            if current_quantity <= restock_level and restock_quantity > 0:
                restocked_products.append(product_id)
                self.restock_product(product_id, restock_quantity)

        if restocked_products:
            # Additional summary notification if multiple products were restocked
            message = "Multiple products restocked:\n\n"
            for pid in restocked_products:
                message += f"Product ID: {pid}\n"
            messagebox.showinfo("Restock Summary", message)
            self.render_table("products")  # Refresh the product table

    # In menu.py
    def restock_product(self, product_id, quantity):
        """Restocks a product with the specified quantity and notifies admin."""
        # Get current product details before restocking
        self.cur.execute(
            "SELECT product_name, quantity, restock_level FROM products WHERE product_id = %s", (product_id,))
        product = self.cur.fetchone()
        product_name, current_quantity, restock_level = product

        # Perform the restocking
        self.cur.execute("UPDATE products SET quantity = quantity + %s WHERE product_id = %s", (quantity, product_id))
        self.con.commit()

        # Calculate new quantity after restocking
        new_quantity = current_quantity + quantity

        # Show notification to biller
        message = f"Product Restocked:\n\n"
        message += f"Product ID: {product_id}\n"
        message += f"Product Name: {product_name}\n"
        message += f"Previous Quantity: {current_quantity}\n"
        message += f"Restocked Quantity: {quantity}\n"
        message += f"New Quantity: {new_quantity}\n"
        message += f"Restock Level: {restock_level}"

        messagebox.showinfo("Restock Notification", message)
        print(f"Restocked {product_id} with {quantity} units")

    # menu.py
    def add_product(self):
        """Creates a new item in inventory by registering the provided details in MySQL."""
        p_id = self.product_entries['Product Id'].get()
        p_name = self.product_entries['Product Name'].get()
        p_desc = self.product_entries['Description'].get()
        p_price = self.product_entries['Price'].get()
        p_qty = self.product_entries['Quantity'].get()
        p_category = self.product_entries['Category'].get()  # Get selected category
        restock_level = self.product_entries['Restock Level'].get()
        restock_quantity = self.product_entries['Restock Quantity'].get()

        # Validation checks
        if not p_id.isdigit():
            error("Product ID must contain only numbers")
            return
        if not p_name.isalpha():
            error("Product Name must contain only characters")
            return
        if not p_desc.isalpha():
            error("Description must contain only characters")
            return
        try:
            float(p_price)
        except ValueError:
            error("Price must be a number")
            return
        try:
            int(p_qty)
        except ValueError:
            error("Quantity must be a number")
            return
        if not p_category:  # Check if category is selected
            error("Please select a category")
            return
        try:
            int(restock_level)
        except ValueError:
            error("Restock Level must be a number")
            return
        try:
            int(restock_quantity)
        except ValueError:
            error("Restock Quantity must be a number")
            return

        self.cur.execute("SELECT * FROM products WHERE product_id = %s", (p_id,))
        f = self.cur.fetchall()
        if f:
            error("Product Id already exists")
        else:
            if len(p_desc) > 50:
                error("Description should be less than 50 letters")
                return
            self.cur.execute(
                "INSERT INTO products VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (p_id, p_name, p_desc, p_price, p_qty, p_category, restock_level, restock_quantity)
            )
            self.con.commit()
            messagebox.showinfo("Item Added!", "Item successfully created!")
            self.topwin.destroy()
            self.tree.delete(*self.tree.get_children())  # Clear current table
            self.render_table("products")  # Refresh table with updated data

    def delete_product(self):
        """Creates a new window to delete a product from the inventory."""
        self.delete_win = ctk.CTkToplevel(self.window)
        self.delete_win.title("Delete Product")
        self.delete_win.geometry("500x300")

        frame = ctk.CTkFrame(master=self.delete_win, width=480, height=280, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        label = ctk.CTkLabel(frame, text="Select Product to Delete:", font=(self.font, 20))
        label.pack(pady=(30, 0))

        # Fetch product names from a database
        self.cur.execute("SELECT product_name FROM products")
        products = self.cur.fetchall()
        product_names = [p[0] for p in products]

        if not product_names:
            error("No products found in inventory.")
            self.delete_win.destroy()
            return

        # Create dropdown menu
        self.product_var = ctk.StringVar(value="")
        combobox = ctk.CTkComboBox(frame, values=product_names, variable=self.product_var, width=300)
        combobox.pack(pady=(20, 30))

        # Add delete button
        delete_btn = ctk.CTkButton(frame, width=200, text="Delete", command=self.confirm_delete, fg_color="#fb0000")
        delete_btn.pack(pady=(0, 20))

    def confirm_delete(self):
        """Confirms and deletes the selected product from the database."""
        product_name = self.product_var.get()
        if not product_name:
            error("Please select a product to delete.")
            return

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {product_name}?"):
            self.cur.execute("DELETE FROM products WHERE product_name = %s", (product_name,))
            self.con.commit()
            messagebox.showinfo("Success", f"{product_name} has been deleted from the inventory.")
            self.delete_win.destroy()  # Close the delete product window
            self.tree.delete(*self.tree.get_children())  # Clear current table
            self.render_table("products")  # Refresh table with updated data

    def generate_invoice(self, order_id, customer_name, items, total_amount, phone_number, address):
        """Generates a PDF invoice with improved layout and formatting."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        elements = []
        styles = getSampleStyleSheet()
        style_heading = styles['Title']
        style_normal = styles['Normal']
        style_bold = styles['BodyText']
        style_bold.fontName = 'Helvetica-Bold'

        # Business information section
        business_frame = [
            Paragraph("INVENTORY MANAGEMENT SYSTEM", style_heading),
            Spacer(1, 12),
            Paragraph("Your Business Name", style_bold),
            Paragraph("GSTIN: 1234567890", style_normal),
            Spacer(1, 12),
            Paragraph(f"Date: {datetime.now().strftime('%d-%m-%Y')}", style_normal),
            Paragraph(f"Invoice No: {order_id}", style_normal),
        ]

        elements.extend(business_frame)
        elements.append(Spacer(1, 24))

        # Customer information section
        customer_frame = [
            Paragraph(f"Customer Name: {customer_name}", style_normal),
            Paragraph(f"Phone Number: {phone_number}", style_normal),  # Added phone number
            Paragraph(f"Address: {address}", style_normal),  # Added address
            Spacer(1, 12),
            Paragraph("--------------------------------------------------", style_normal),
            Spacer(1, 12),
        ]

        elements.extend(customer_frame)

        # Table data with GST details
        data = [
            ['Product Name', 'Base Price', 'Quantity', 'CGST', 'SGST', 'Final Price']
        ]

        total_cgst = 0
        total_sgst = 0
        total_tax = 0

        for item in items:
            product_id = item[0]
            product_name = item[1]
            base_price = float(item[3])
            quantity = int(item[4])

            # Get tax rates from database
            self.cur.execute("SELECT category FROM products WHERE product_id = %s", (product_id,))
            category = self.cur.fetchone()[0]
            self.cur.execute("SELECT CGST, SGST FROM categories WHERE category_name = %s", (category,))
            tax_rates = self.cur.fetchone()

            if not tax_rates:
                error(f"No tax rates found for category {category}")
                return

            # Convert Decimal to float
            cgst_percent = float(tax_rates[0])
            sgst_percent = float(tax_rates[1])

            # Calculate tax amounts
            cgst_amount = (base_price * cgst_percent / 100)
            sgst_amount = (base_price * sgst_percent / 100)
            total_tax_amount = cgst_amount + sgst_amount
            final_price = base_price + total_tax_amount
            final_price1=final_price * quantity
            
            # Add to totals
            total_cgst += cgst_amount * quantity
            total_sgst += sgst_amount * quantity
            total_tax += total_tax_amount * quantity

            # Add to invoice items
            data.append([
                Paragraph(product_name, style_normal),
                Paragraph(f"{base_price:.2f} Rs", style_normal),
                Paragraph(str(quantity), style_normal),
                Paragraph(f"{cgst_amount:.2f} Rs", style_normal),
                Paragraph(f"{sgst_amount:.2f} Rs", style_normal),
                Paragraph(f"{final_price:.2f} Rs", style_normal)
            ])

        # Add total row
        data.append([
            Paragraph("", style_normal),
            Paragraph("", style_normal),
            Paragraph("", style_normal),
            Paragraph(f"Total CGST: {total_cgst:.2f} Rs", style_bold),
            Paragraph(f"Total SGST: {total_sgst:.2f} Rs", style_bold),
            Paragraph(f"Total Amount: {final_price1:.2f} Rs", style_bold)
        ])

        # Create table with improved styling
        table = Table(data, colWidths=[2.5 * inch, 1.2 * inch, 0.8 * inch, 1.2 * inch, 1.2 * inch, 1.5 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
            ('LINEABOVE', (0, 1), (-1, -2), 0.25, colors.grey),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 24))

        # Payment information section
        payment_frame = [
            Paragraph(f"Date of Actual Payment: {datetime.now().strftime('%d-%m-%Y')}", style_normal),
            Spacer(1, 12),
            Paragraph("Thank you for your business!", style_normal),
        ]

        elements.extend(payment_frame)

        # Build the PDF
        doc.build(elements)

        # Save the PDF to a file
        pdf_name = f"Invoice_{order_id}.pdf"
        with open(pdf_name, "wb") as f:
            f.write(buffer.getvalue())

        # Open the PDF file
        if os.name == 'nt':
            os.startfile(pdf_name)
        else:
            os.system(f'xdg-open "{pdf_name}"')

        messagebox.showinfo("Invoice Generated", f"Invoice {order_id} has been generated successfully.")


    def logout(self):
        self.login_win.destroy()
        self._logged_out = True


    def render_table(self, table=None, items=None, query=None):
        """Render data from the database table into a Tkinter TreeView."""
        if query:
            self.cur.execute(query)
            items = self.cur.fetchall()

        if not items:
            self.cur.execute(f"SELECT * FROM {table};")
            items = self.cur.fetchall()

        # Clear existing items in the tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Process each item to hide sensitive information for 'USER' type
        for item in items:
            # Check if the user is of type 'USER' and hide password and email
            if item[2] == 'USER':  # Assuming the third column is 'account_type'
                # Replace password and email with ***
                modified_item = list(item)
                modified_item[1] = "***"  # Replace password
                modified_item[3] = "***"  # Replace email
                item = tuple(modified_item)

            self.tree.insert('', 'end', values=item)
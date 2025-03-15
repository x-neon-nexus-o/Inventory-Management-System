import tkinter
from tkinter import ttk, messagebox
from datetime import date
import customtkinter as ctk
from PIL import Image

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
        self.make_window()

    def make_window(self):
        """ Create window to display menu"""
        width = 1350
        height = 740
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.window.geometry("%dx%d+%d+%d" % (width, height, x, y))
        self.login_win.withdraw()
        self.make_panel()

    def make_panel(self):
        """ Create side panel or navigation panel"""
        side_panel = ctk.CTkFrame(self.window, corner_radius=0, width=250)
        side_panel.pack(fill="y", side="left")

        section_functions = {
            "dashboard": self.dashboard,
            "inventory": self.inventory,
            "orders": self.orders,
            "users": self.users,
            "shop": self.shop,
            "history": self.history,
            "logout": self.logout
        }

        # Add buttons for different sections in the side panel
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
        x = 50
        self.cur.execute("SELECT COUNT(*) FROM orders WHERE Date(date) = Curdate();")
        sales = self.cur.fetchall()[0]
        self.cur.execute("SELECT COUNT(*) FROM orders;")
        transactions = self.cur.fetchall()[0]
        self.cur.execute("SELECT COUNT(*) FROM products;")
        items = self.cur.fetchall()[0]

        header = {"Total Sales Today": sales, "Total Transactions": transactions, "Items in Inventory": items}
        for title in header:
            frame = ctk.CTkFrame(master=self.frame, width=300, height=150, corner_radius=15, fg_color="#007fff")
            frame.place(x=x, y=100)

            label = ctk.CTkLabel(self.frame, text=header[title], fg_color="#007fff", font=(self.font, 50))
            label.place(x=x + 130, y=130)

            text = ctk.CTkLabel(self.frame, text=title, fg_color="#007fff", font=(self.font, 20))
            text.place(x=x + 60, y=220)

            x += 350
        try:
            add_graphs(self.cur, self.frame)
        except:
            pass

    # menu.py
    # menu.py
    def inventory(self):
        """ Displays the inventory section of the user interface. """
        self.set_title("Inventory")
        if self.user[2] == 'ADMIN':
            add_button = ctk.CTkButton(self.frame, width=100, command=self.add_button, text="Add Item",
                                       fg_color="#007fff", font=(self.font, 20))
            add_button.place(x=50, y=50)

            # Add delete button next to add button
            delete_button = ctk.CTkButton(self.frame, width=100, command=self.delete_product, text="Delete Item",
                                          fg_color="#fb0000", font=(self.font, 20))
            delete_button.place(x=170, y=50)
        self.make_table(("Product ID", "Product Name", "Description", "Price", "Quantity", "Category"), 130, "products")

    def make_table(self, col, width, table=None, height=600):
        """Create a tkinter treeview table with specified columns, column widths, and optional data source table.

            Args:
                col (tuple): Tuple of column names.
                width (list): List of column widths.
                table (str, optional): Name of the table. Defaults to None.
                height (int, optional): Height of the table. Defaults to 600.
        """
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
        headings = ("Product Id", "Product Name", "Description", "Price", "Quantity", "Total Amount")
        self.make_table(headings, 130, height=400)

    def orders(self):
        """ Displays all the Orders placed in the system."""
        self.set_title("Orders")
        headings = ("Order Id", "User", "Date", "Total Items", "Total Amount", "Payment Status")
        self.make_table(headings, 130, "orders")

    def history(self):
        """ Displays the order history of the user. """
        self.set_title("Transactions History")
        headings = ("Order Id", "Product Name", "Quantity", "Price", "Date", "Payment Status")
        query = f'''SELECT o.order_id , p.product_name, oi.quantity , oi.price , o.date, o.payment_status
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        WHERE o.user = '{self.user[0]}';
        '''
        self.make_table(headings, 130)
        self.render_table(query=query)

    def add_item(self):
        """Display another window to add items to cart"""
        new_win = ctk.CTkToplevel(self.window)
        new_win.title("Add item to Cart")
        new_win.geometry("500x500")

        self.win_frame = ctk.CTkFrame(master=new_win, width=480, height=480, corner_radius=15)
        self.win_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.item_var = ctk.StringVar(value="")

        label = ctk.CTkLabel(self.win_frame, text="Select Item :", font=(self.font, 20))
        label.place(x=50, y=50)

        self.cur.execute("SELECT product_name FROM products")
        products = self.cur.fetchall()
        product_names = [p[0] for p in products]
        combobox = ctk.CTkComboBox(self.win_frame, values=product_names, command=self.fill_labels,
                                   variable=self.item_var, width=200)
        combobox.place(x=250, y=50)
        labels = ['Available Quantity', 'Unit Price', 'Quantity']
        x, y = 50, 100
        self.entries = {}
        for i in labels:
            label = ctk.CTkLabel(self.win_frame, text=f"{i} :", font=(self.font, 20))
            label.place(x=x, y=y)
            y += 60

        button = ctk.CTkButton(master=self.win_frame, width=400, text="Add", corner_radius=6, command=self.add_to_cart)
        button.place(x=25, y=340)

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
            self.cur.execute(f"UPDATE products SET quantity = quantity + {qty} WHERE product_id = '{p_id}';")
            self.con.commit()
        self.total()

    def fill_labels(self, choice):
        """ Fills labels with data of a particular item chosen by user"""
        self.cur.execute(f"SELECT quantity, price  FROM products WHERE product_name='{choice}';")
        fetch = self.cur.fetchall()[0]
        self.spin_var = ctk.IntVar(value=1)
        x = 250
        try:
            self.price_label.place_forget()
            self.quantity_label.place_forget()
            self.spinbox.place_forget()
        except:
            pass

        self.quantity_label = ctk.CTkLabel(self.win_frame, text=fetch[0], font=(self.font, 20))
        self.quantity_label.place(x=x, y=100)
        self.price_label = ctk.CTkLabel(self.win_frame, text=fetch[1], font=(self.font, 20))
        self.price_label.place(x=x, y=160)

        style = ttk.Style()
        style.configure("TSpinbox", fieldbackground="#343638", foreground="white", background="#343638")

        self.spinbox = ttk.Spinbox(self.win_frame, from_=1, to=fetch[0], textvariable=self.spin_var, style="TSpinbox")
        self.spinbox.place(x=x, y=345)

    def add_to_cart(self):
        """ Adds selected items to the shopping cart."""
        try:
            name = self.item_var.get()
            if name == '':
                error("Select an Item to add")
                return
            qty = self.spin_var.get()
            if qty <= 0 or self.quantity_label.cget('text') <= 0 or self.quantity_label.cget('text') <= qty:
                error('Enter a valid Quantity')
                return
        except:
            return
        self.cur.execute(f"SELECT product_id , description , price from products where product_name='{name}';")
        p_id, desc, price = self.cur.fetchall()[0]

        self.cur.execute(f"UPDATE products SET quantity = quantity - {qty} WHERE product_id = '{p_id}';")
        self.con.commit()
        self.fill_labels(name)

        amount = self.price_label.cget("text") * qty
        items = [(p_id, name, desc, price, qty, amount)]
        self.render_table(items=items)
        self.total()

    def total(self):
        """Evaluates the total amount in cart and displays it"""
        total = round(sum(float(self.tree.item(item, "values")[-1]) for item in self.tree.get_children()), 2)
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
            entry = ctk.CTkEntry(master=frame, placeholder_text=i, width=350, height=35)
            entry.pack(pady=(0, 10))
            self.product_entries[i] = entry

        # Place the "Add" button below the entry fields
        button = ctk.CTkButton(master=frame, width=400, text="Add", corner_radius=6, command=self.add_product)
        button.pack(pady=20)  # Use pack for simplicity

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

        query = 'select order_id from orders;'
        self.cur.execute(query)
        rows = self.cur.fetchall()
        count = self.cur.rowcount
        if count == 0:
            order_id = 1001  # first account no is 1001
        else:
            order_id = rows[-1][0] + 1

        query = 'select order_item_id from order_items;'
        self.cur.execute(query)
        rows = self.cur.fetchall()
        count = self.cur.rowcount
        if count == 0:
            order_item_id = 1  # first account no is 1
        else:
            order_item_id = rows[-1][0] + 1
        for item in all_items:
            values = self.tree.item(item, "values")
            product_id = values[0]
            quantity = values[-2]
            price = values[-1]
            self.cur.execute(
                f"INSERT INTO order_items (order_item_id ,order_id, product_id, quantity, price) VALUES ({order_item_id}, {order_id}, '{product_id}',{quantity}, {price})")
            order_item_id += 1

        total_amount = sum(float(self.tree.item(item, "values")[-1]) for item in all_items)
        total_items = len(all_items)
        self.cur.execute(
            f"INSERT INTO orders (order_id, user, date, total_items ,total_amount, payment_status) VALUES ({order_id}, '{self.user[0]}', '{date.today()}', {total_items},{total_amount}, '{payment_status}')")

        self.con.commit()

        # Check if any product needs restocking
        self.check_and_restock_products()

        messagebox.showinfo("Success", "Order placed successfully.")
        self.tree.delete(*self.tree.get_children())

    def check_and_restock_products(self):
        """Checks if any products need restocking and restocks them if necessary."""
        self.cur.execute("SELECT product_id, quantity, restock_level, restock_quantity FROM products")
        products = self.cur.fetchall()
        for product in products:
            product_id, current_quantity, restock_level, restock_quantity = product
            if current_quantity <= restock_level and restock_quantity > 0:
                self.restock_product(product_id, restock_quantity)

    # In menu.py

    def restock_product(self, product_id, quantity):
        """Restocks a product with the specified quantity and notifies admin."""
        # Get current product details before restocking
        self.cur.execute(
            f"SELECT product_name, quantity, restock_level FROM products WHERE product_id = '{product_id}'")
        product = self.cur.fetchone()
        product_name, current_quantity, restock_level = product

        # Perform the restocking
        self.cur.execute(f"UPDATE products SET quantity = quantity + {quantity} WHERE product_id = '{product_id}'")
        self.con.commit()

        # Calculate new quantity after restocking
        new_quantity = current_quantity + quantity

        # Show notification to admin
        message = f"Product Restocked:\n\n"
        message += f"Product ID: {product_id}\n"
        message += f"Product Name: {product_name}\n"
        message += f"Previous Quantity: {current_quantity}\n"
        message += f"Restocked Quantity: {quantity}\n"
        message += f"New Quantity: {new_quantity}\n"
        message += f"Restock Level: {restock_level}"

        messagebox.showinfo("Restock Notification", message)
        print(f"Restocked {product_id} with {quantity} units")

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

    # menu.py
    def add_product(self):
        """Creates a new item in inventory by registering the provided details in MySQL."""
        p_id = self.product_entries['Product Id'].get()
        p_name = self.product_entries['Product Name'].get()
        p_desc = self.product_entries['Description'].get()
        p_price = self.product_entries['Price'].get()
        p_qty = self.product_entries['Quantity'].get()
        p_category = self.product_entries['Category'].get()
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
        if not p_category.isalpha():
            error("Category must contain only characters")
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

        self.cur.execute(f"select * from products where product_id='{p_id}'")
        f = self.cur.fetchall()
        if f:
            error("Product Id already exists")
        else:
            if len(p_desc) > 50:
                error("Description should be less than 50 letters")
                return
            self.cur.execute(
                f"insert into products values('{p_id}','{p_name}','{p_desc}',{p_price},{p_qty},'{p_category}', {restock_level}, {restock_quantity})")
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

        # Fetch product names from database
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
            self.cur.execute(f"DELETE FROM products WHERE product_name = '{product_name}'")
            self.con.commit()
            messagebox.showinfo("Success", f"{product_name} has been deleted from the inventory.")
            self.delete_win.destroy()  # Close the delete product window
            self.tree.delete(*self.tree.get_children())  # Clear current table
            self.render_table("products")  # Refresh table with updated data

    def logout(self):
        self.login_win.destroy()
        self.logout = True

    # menu.py
    def make_table(self, col, width, table=None, height=400):
        """Create a tkinter treeview table with specified columns, column widths, and optional data source table.

            Args:
                col (tuple): Tuple of column names.
                width (list): List of column widths.
                table (str, optional): Name of the table. Defaults to None.
                height (int, optional): Height of the table. Defaults to 400.
        """
        tableframe = ctk.CTkScrollableFrame(self.frame, width=1000, height=height)
        tableframe.place(x=1070, y=100, anchor=tkinter.NE)  # Adjusted y position to 100
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

    # menu.py
    def render_table(self, table=None, items=None, query=None):
        """Render data from the database table into a Tkinter TreeView.
            Args:
                table (str, optional): Name of the table. Defaults to None.
                items (list, optional): items of the table. Defaults to None.
                query (list, optional): custom sql query. Defaults to None.
        """
        if query:
            self.cur.execute(query)
            items = self.cur.fetchall()

        if not items:
            self.cur.execute(f"SELECT * FROM {table};")
            items = self.cur.fetchall()

        # Clear existing items in the tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        for item in items:
            self.tree.insert('', 'end', values=item)
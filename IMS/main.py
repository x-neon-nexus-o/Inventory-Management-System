# main.py
import mysql.connector as mycon
from login import Login
from menu import Menu

class Main:
    def __init__(self):
        self.con = mycon.connect(host='localhost', user='root', passwd='manager')
        if self.con.is_connected:
            print('* Connected to MySQL server')
            self.cur = self.con.cursor()
        else:
            print('[!]  Not connected to MySQL')

        db_query = "CREATE DATABASE IF NOT EXISTS inventory"
        self.cur.execute(db_query)

        self.con.database = 'inventory'
        self.cur.execute("CREATE TABLE if not exists users (username varchar (20) PRIMARY KEY, password varchar (20) NOT NULL, account_type varchar (10) NOT NULL, email varchar (50) NOT NULL);")
        self.cur.execute("CREATE TABLE if not exists products (product_id varchar (20) PRIMARY KEY, product_name varchar (50) NOT NULL, description varchar (50) NOT NULL, price DECIMAL(10, 2) NOT NULL, quantity INTEGER NOT NULL, category varchar (50) NOT NULL, restock_level INTEGER, restock_quantity INTEGER);")
        self.cur.execute("CREATE TABLE if not exists orders (order_id INTEGER PRIMARY KEY, user varchar (20), date DATE, total_items INTEGER, total_amount DECIMAL(10, 2), payment_status varchar(20), customer_name varchar(100), phone_number varchar(20), address varchar(100));")
        self.cur.execute("CREATE TABLE if not exists order_items (order_item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id varchar (20), quantity INTEGER NOT NULL, price DECIMAL(10, 2) NOT NULL);")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS categories (category_name VARCHAR(50) PRIMARY KEY,GST DECIMAL(5, 2) NOT NULL,SGST DECIMAL(5, 2) NOT NULL,CGST DECIMAL(5, 2) NOT NULL)""")
        self.login = Login(self.con)
        self.login.window.mainloop()
        if self.login.user:
            self.menu = Menu(self.con, self.login.user, self.login.window)
            self.menu.window.mainloop()

            if self.menu.logout == True:
                Main()

if __name__ == "__main__":
    m = Main()
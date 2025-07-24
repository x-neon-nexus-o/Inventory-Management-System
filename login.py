import tkinter
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image

from utils import error


class Login:
    """Represents a login window for user authentication."""

    def __init__(self, con):
        ctk.set_default_color_theme("dark-blue")
        ctk.set_appearance_mode("dark")
        self.window = ctk.CTk()
        self.window.title("Sign In")
        self.window.geometry("500x600")
        self.con = con
        self.cur = con.cursor()
        self.user = None
        self.login_window()

    def login_window(self, event=None):
        """ Function to create login window."""
        self.window.title("Sign In")
        self.window.bind('<Return>', self.login)

        img = ctk.CTkImage(dark_image=Image.open("./imgs/bg.jpg").resize((500, 600)), size=(500, 600))
        bg = ctk.CTkLabel(master=self.window, image=img)
        bg.place(x=0, y=0)

        self.frame = ctk.CTkFrame(master=bg, width=320, height=360, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.login_label = ctk.CTkLabel(master=self.frame, text="Log in", font=('Century Gothic', 30))
        self.login_label.place(x=120, y=45)

        self.username = ctk.CTkEntry(master=self.frame, width=220, placeholder_text='Username')
        self.username.place(x=50, y=110)

        self.password = ctk.CTkEntry(master=self.frame, width=220, placeholder_text='Password', show="*")
        self.password.place(x=50, y=165)

        # Registration prompt label placed above forgot password link
        self.label_link = ctk.CTkLabel(master=self.frame, text="Not registered as biller? Register It",
                                       font=('Century Gothic', 13))
        self.label_link.place(x=60, y=210)
        self.label_link.bind("<Button-1>", self.register_window)

        # Forgot password link placed below registration prompt
        self.forgot_password_link = ctk.CTkLabel(master=self.frame, text="Forgot Password?",
                                                 font=('Century Gothic', 13))
        self.forgot_password_link.place(x=160, y=235)  # Adjusted y-coordinate to place below registration prompt
        self.forgot_password_link.bind("<Button-1>", lambda e: self.forgot_password())

        # Create Login button and assign to instance variable
        self.login_button = ctk.CTkButton(master=self.frame, width=220, text="Login", command=self.login,
                                          corner_radius=6)
        self.login_button.place(x=50, y=270)  # Adjusted y-coordinate to accommodate label changes

    # In the register_window method, hide the labels
    def register_window(self, event=None):
        """ Function to display register window."""
        self.window.title("Create an account")
        self.window.bind('<Return>', self.register)
        self.login_label.configure(text="Register")
        self.label_link.configure(text="Already have an Account? Sign in")
        self.label_link.bind("<Button-1>", self.login_window)

        # Add email field
        self.email = ctk.CTkEntry(master=self.frame, width=220, placeholder_text='Email')
        self.email.place(x=50, y=220)

        # Create Continue button and store as instance variable
        self.continue_button = ctk.CTkButton(master=self.frame, width=220, text="Continue", command=self.register,
                                             corner_radius=6)
        self.continue_button.place(x=50, y=275)

        # Hide the login button
        self.login_button.place_forget()

        # Add Back button
        self.back_button = ctk.CTkButton(master=self.frame, width=100, text="Back", command=self.show_login_window,
                                         corner_radius=6)
        self.back_button.place(x=50, y=320)

        # Hide the registration prompt and forgot password link
        self.label_link.place_forget()
        self.forgot_password_link.place_forget()

    # In the show_login_window method, show the labels again
    def show_login_window(self):
        """ Function to switch back to login window from register window."""
        # Clear registration elements
        try:
            self.email.place_forget()
        except:
            pass
        try:
            self.continue_button.place_forget()
        except:
            pass
        try:
            self.back_button.place_forget()
        except:
            pass

        # Show login elements again
        self.login_label.configure(text="Log in")
        self.label_link.configure(text="Not registered as biller? Register It")
        self.label_link.bind("<Button-1>", self.register_window)

        # Show the login button
        self.login_button.place(x=50, y=250)

        # Show the registration prompt and forgot password link
        self.label_link.place(x=60, y=210)
        self.forgot_password_link.place(x=160, y=210)

        # Change window title back to login
        self.window.title("Sign In")
        self.window.bind('<Return>', self.login)

    def login(self, event=None):
        """Authenticate the user by checking the provided username and password with MySQL. """
        uname = self.username.get()
        pwd = self.password.get()
        self.cur.execute(
            "INSERT IGNORE INTO users (username, password, account_type, email) VALUES ('ADMIN', 'ADMIN', 'ADMIN', 'admin@example.com');")
        self.cur.execute(f"select * from users where username='{uname}' and password='{pwd}' ")
        f = self.cur.fetchall()
        if f:
            print("└─Logged in as {}".format(uname))
            self.window.quit()
            self.user = f[0]

        else:
            error("Invalid Username or Password")

    def register(self):
        """Create a new user account by registering the provided username and password in MySQL. """
        uname = self.username.get()
        pwd = self.password.get()
        email = self.email.get()

        self.cur.execute(f"select * from users where username='{uname}'")
        f = self.cur.fetchall()
        if f:
            error("Username already exist")
        else:
            if (len(uname) == 0 or len(pwd) == 0 or len(email) == 0):
                error("All fields are required")
                return
            elif len(uname) > 20 or len(pwd) > 20:
                error("Length of the Username and Password should be less than 20")
                return

            self.cur.execute(f"insert into users values('{uname}','{pwd}','USER', '{email}')")
            self.con.commit()
            messagebox.showinfo("Account created", "Your account has been succesfully created!")
            self.window.quit()
            self.user = (uname, pwd, 'USER', email)

    def forgot_password(self):
        """ Function to handle forgot password functionality."""
        self.window.title("Forgot Password")
        self.frame.destroy()

        self.frame = ctk.CTkFrame(master=self.window, width=320, height=420, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.forgot_label = ctk.CTkLabel(master=self.frame, text="Forgot Password", font=('Century Gothic', 30))
        self.forgot_label.place(x=50, y=45)

        self.username = ctk.CTkEntry(master=self.frame, width=220, placeholder_text='Username')
        self.username.place(x=50, y=110)

        self.email = ctk.CTkEntry(master=self.frame, width=220, placeholder_text='Email')
        self.email.place(x=50, y=165)

        self.new_password = ctk.CTkEntry(master=self.frame, width=220, placeholder_text='New Password', show="*")
        self.new_password.place(x=50, y=220)

        self.confirm_password = ctk.CTkEntry(master=self.frame, width=220, placeholder_text='Confirm Password',
                                             show="*")
        self.confirm_password.place(x=50, y=275)

        button = ctk.CTkButton(master=self.frame, width=220, text="Reset Password", command=self.reset_password,
                               corner_radius=6)
        button.place(x=50, y=330)

        back_button = ctk.CTkButton(master=self.frame, width=100, text="Back", command=self.login_window,
                                    corner_radius=6)
        back_button.place(x=50, y=380)

    def reset_password(self):
        """ Function to reset user's password."""
        uname = self.username.get()
        email = self.email.get()
        new_pwd = self.new_password.get()
        confirm_pwd = self.confirm_password.get()

        if new_pwd != confirm_pwd:
            error("Passwords do not match")
            return

        self.cur.execute(f"select * from users where username='{uname}' and email='{email}'")
        user = self.cur.fetchone()
        if user:
            self.cur.execute(f"update users set password='{new_pwd}' where username='{uname}'")
            self.con.commit()
            messagebox.showinfo("Success", "Password reset successfully!")
            self.login_window()
        else:
            error("Invalid username or email")

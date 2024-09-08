from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import mysql.connector

class Database:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="entrance_exam"
        )
        self.cursor = self.db.cursor()

    def query(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())
        self.db.commit()

class LoginPage(tk.Frame):
    def __init__(self, root, db):
        super().__init__(root)
        self.root = root
        self.db = db
        self.root.title("Course Exam Recommendation System")
        self.root.geometry("900x600")
        self.current_user_account_type = None
        self.login_form()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_form(self):
        self.clear_frame()

        # Load and display the image
        img_path = "images/Cmi.JPG"  # Update this path based on your findings
        try:
            img = ImageTk.PhotoImage(Image.open(img_path))
        except Exception as e:
            print(f"Error loading image: {e}")
            img = None

        if img is not None:
            panel = tk.Label(self.root, image=img, bg="#f0f0f0")
            panel.image = img  # Keep a reference to the image to avoid garbage collection
            panel.pack(side="bottom", fill="both", expand="yes")

        self.login_frame = tk.Frame(self.root, bg="light blue")
        self.login_frame.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        tk.Label(self.login_frame, text="Log in", font=("Helvetica", 24, "bold"), bg="light blue").pack(pady=10)

        tk.Label(self.login_frame, text="Username:", bg="light blue").pack()
        self.entry_username = tk.Entry(self.login_frame)
        self.entry_username.pack(pady=5)

        tk.Label(self.login_frame, text="Password:", bg="light blue").pack()
        self.entry_password = tk.Entry(self.login_frame, show="*")
        self.entry_password.pack(pady=5)

        tk.Button(self.login_frame, text="Login", bg="white", command=self.authenticate_user).pack(pady=10)
        tk.Button(self.login_frame, text="Create Account", bg="white", command=self.create_user_form).pack(pady=10)

        self.root.config(bg="light gray")

    def authenticate_user(self):
        # Placeholder for authentication logic
        username = self.entry_username.get()
        password = self.entry_password.get()
        print(f"Authenticating user: {username}")

        # You can add your database authentication logic here
        # Example:
        result = self.db.query("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        if result:
            messagebox.showinfo("Login Successful", "Welcome!")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def create_user_form(self):
        # Placeholder for creating user form logic
        print("Creating user form...")

if __name__ == "__main__":
    root = tk.Tk()
    db = Database()
    app = LoginPage(root, db)
    root.mainloop()

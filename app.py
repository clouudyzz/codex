import tkinter as tk
from tkinter import messagebox
import json
import os
import hashlib

USER_FILE = 'users.json'

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

class AuthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auth Application")
        self.users = load_users()

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)

        self.mode = 'login'
        self.build_login()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def build_login(self):
        self.mode = 'login'
        self.clear_frame()

        tk.Label(self.main_frame, text="Login", font=('Arial', 16)).grid(row=0, column=0, columnspan=2, pady=5)
        tk.Label(self.main_frame, text="Username:").grid(row=1, column=0, sticky='e')
        self.username_entry = tk.Entry(self.main_frame)
        self.username_entry.grid(row=1, column=1)

        tk.Label(self.main_frame, text="Password:").grid(row=2, column=0, sticky='e')
        self.password_entry = tk.Entry(self.main_frame, show='*')
        self.password_entry.grid(row=2, column=1)

        tk.Button(self.main_frame, text="Login", command=self.login).grid(row=3, column=0, columnspan=2, pady=5)
        tk.Button(self.main_frame, text="Go to Register", command=self.build_register).grid(row=4, column=0, columnspan=2)

    def build_register(self):
        self.mode = 'register'
        self.clear_frame()

        tk.Label(self.main_frame, text="Register", font=('Arial', 16)).grid(row=0, column=0, columnspan=2, pady=5)
        tk.Label(self.main_frame, text="Username:").grid(row=1, column=0, sticky='e')
        self.reg_username_entry = tk.Entry(self.main_frame)
        self.reg_username_entry.grid(row=1, column=1)

        tk.Label(self.main_frame, text="Email:").grid(row=2, column=0, sticky='e')
        self.reg_email_entry = tk.Entry(self.main_frame)
        self.reg_email_entry.grid(row=2, column=1)

        tk.Label(self.main_frame, text="Password:").grid(row=3, column=0, sticky='e')
        self.reg_password_entry = tk.Entry(self.main_frame, show='*')
        self.reg_password_entry.grid(row=3, column=1)

        tk.Button(self.main_frame, text="Register", command=self.register).grid(row=4, column=0, columnspan=2, pady=5)
        tk.Button(self.main_frame, text="Go to Login", command=self.build_login).grid(row=5, column=0, columnspan=2)

    def register(self):
        username = self.reg_username_entry.get().strip()
        email = self.reg_email_entry.get().strip()
        password = self.reg_password_entry.get()

        if not username or not password or not email:
            messagebox.showerror("Error", "All fields are required")
            return
        if username in self.users:
            messagebox.showerror("Error", "Username already exists")
            return

        self.users[username] = {
            'email': email,
            'password': hash_password(password)
        }
        save_users(self.users)
        messagebox.showinfo("Success", "Registration successful")
        self.build_login()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if username not in self.users:
            messagebox.showerror("Error", "User not found")
            return
        stored_password = self.users[username]['password']
        if stored_password != hash_password(password):
            messagebox.showerror("Error", "Incorrect password")
            return

        messagebox.showinfo("Success", f"Welcome, {username}!")

if __name__ == '__main__':
    root = tk.Tk()
    app = AuthApp(root)
    root.mainloop()

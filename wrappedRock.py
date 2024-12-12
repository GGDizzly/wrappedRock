import customtkinter as ctk
from tkinter import filedialog
from datetime import datetime
import sqlite3
import os

# Database setup
connection = sqlite3.connect("wrappedRock.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS climbs (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    grade TEXT,
    moves INTEGER,
    file_path TEXT,
    likes INTEGER DEFAULT 0,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

ctk.set_appearance_mode("Dark")  # Options: "System", "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Ensure theme is valid: "blue", "green", "dark-blue"

class Climbs:
    def __init__(self, grade, numOfMoves, file_path=None):
        self.grade = grade
        self.numOfMoves = numOfMoves
        self.file_path = file_path
        self.timestamp = datetime.now()

    @staticmethod
    def pick_file():
        return filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("Video Files", "*.mp4;*.avi;*.mov"), ("Image Files", "*.png;*.jpg;*.jpeg")]
        )

class WrappedRock(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Wrapped Rock")
        self.geometry("1000x700")
        self.username = None  # To store logged-in user's username

        self.bottom_nav = ctk.CTkFrame(self, height=50, fg_color="gray")
        self.bottom_nav.pack(side="bottom", fill="x")

        self.add_navigation_buttons()
        self.create_login_page()

    def add_navigation_buttons(self):
        for widget in self.bottom_nav.winfo_children():
            widget.destroy()

        ctk.CTkButton(self.bottom_nav, text="Feed", command=self.create_feed_page).pack(side="left", expand=True, padx=5, pady=5)
        ctk.CTkButton(self.bottom_nav, text="Profile", command=self.create_profile_page).pack(side="left", expand=True, padx=5, pady=5)
        ctk.CTkButton(self.bottom_nav, text="Trending", command=self.create_trending_page).pack(side="left", expand=True, padx=5, pady=5)
        ctk.CTkButton(self.bottom_nav, text="Look Up Users", command=self.create_lookup_users_page).pack(side="left", expand=True, padx=5, pady=5)

    def create_login_page(self):
        for widget in self.winfo_children():
            if widget != self.bottom_nav:
                widget.destroy()

        frame = ctk.CTkFrame(self)
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="Login").pack(pady=10)

        entry_frame = ctk.CTkFrame(frame)
        entry_frame.pack(pady=10)

        self.username_entry = ctk.CTkEntry(entry_frame, placeholder_text="Username")
        self.username_entry.pack(pady=5)

        self.password_entry = ctk.CTkEntry(entry_frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=5)

        button_frame = ctk.CTkFrame(frame)
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="Login", command=self.login).pack(pady=5)
        ctk.CTkButton(button_frame, text="Register", command=self.create_register_page).pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            self.username = username
            self.create_main_page()
        else:
            ctk.CTkLabel(self, text="Login Failed. Try again.").pack(pady=10)

    def create_register_page(self):
        for widget in self.winfo_children():
            if widget != self.bottom_nav:
                widget.destroy()

        frame = ctk.CTkFrame(self)
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="Register").pack(pady=10)

        entry_frame = ctk.CTkFrame(frame)
        entry_frame.pack(pady=10)

        self.username_entry = ctk.CTkEntry(entry_frame, placeholder_text="Username")
        self.username_entry.pack(pady=5)

        self.password_entry = ctk.CTkEntry(entry_frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=5)

        button_frame = ctk.CTkFrame(frame)
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="Register", command=self.register).pack(pady=5)
        ctk.CTkButton(button_frame, text="Back", command=self.create_login_page).pack(pady=5)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            ctk.CTkLabel(self, text="Username already taken.").pack(pady=10)
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            connection.commit()
            ctk.CTkLabel(self, text="Registration Successful.").pack(pady=10)
            self.create_login_page()

    def create_main_page(self):
        for widget in self.winfo_children():
            if widget != self.bottom_nav:
                widget.destroy()

        ctk.CTkLabel(self, text=f"Welcome, {self.username}!").pack(pady=10)

    def create_feed_page(self):
        for widget in self.winfo_children():
            if widget != self.bottom_nav:
                widget.destroy()

        ctk.CTkLabel(self, text="Friends' Feed").pack(pady=10)

        scrollbox = ctk.CTkScrollableFrame(self)
        scrollbox.pack(pady=10)

        # Fetch climbs from friends (placeholder for database query)
        feed_climbs = [
            {"user": "friend1", "grade": "V5", "moves": 10, "file": "path/to/video.mp4"},
            {"user": "friend2", "grade": "V4", "moves": 8, "file": "path/to/image.jpg"},
        ]

        for post in feed_climbs:
            post_text = f"{post['user']} - Grade: {post['grade']}, Moves: {post['moves']}"
            ctk.CTkLabel(scrollbox, text=post_text).pack(pady=5)

            if post["file"]:
                ctk.CTkButton(scrollbox, text="View File", command=lambda path=post["file"]: self.open_file(path)).pack(pady=5)

    def create_profile_page(self):
        for widget in self.winfo_children():
            if widget != self.bottom_nav:
                widget.destroy()

        ctk.CTkLabel(self, text=f"{self.username}'s Profile").pack(pady=10)

        scrollbox = ctk.CTkScrollableFrame(self)
        scrollbox.pack(pady=10)

        # Fetch user climbs (placeholder for database query)
        user_climbs = [
            {"grade": "V6", "moves": 12, "file": "path/to/climb1.mp4"},
            {"grade": "V4", "moves": 8, "file": "path/to/climb2.jpg"},
        ]

        for climb in user_climbs:
            climb_text = f"Grade: {climb['grade']}, Moves: {climb['moves']}"
            ctk.CTkLabel(scrollbox, text=climb_text).pack(pady=5)

            if climb["file"]:
                ctk.CTkButton(scrollbox, text="View File", command=lambda path=climb["file"]: self.open_file(path)).pack(pady=5)

    def create_trending_page(self):
        for widget in self.winfo_children():
            if widget != self.bottom_nav:
                widget.destroy()

        ctk.CTkLabel(self, text="Trending Climbs").pack(pady=10)

        scrollbox = ctk.CTkScrollableFrame(self)
        scrollbox.pack(pady=10)

        # Fetch trending climbs (placeholder for database query)
        trending_climbs = [
            {"user": "user1", "grade": "V7", "likes": 50, "file": "path/to/trending1.mp4"},
            {"user": "user2", "grade": "V6", "likes": 40, "file": "path/to/trending2.jpg"},
        ]

        for climb in trending_climbs:
            climb_text = f"{climb['user']} - Grade: {climb['grade']}, Likes: {climb['likes']}"
            ctk.CTkLabel(scrollbox, text=climb_text).pack(pady=5)

            if climb["file"]:
                ctk.CTkButton(scrollbox, text="View File", command=lambda path=climb["file"]: self.open_file(path)).pack(pady=5)

    def create_lookup_users_page(self):
        for widget in self.winfo_children():
            if widget != self.bottom_nav:
                widget.destroy()

        ctk.CTkLabel(self, text="Look Up Users").pack(pady=10)

        search_entry = ctk.CTkEntry(self, placeholder_text="Enter username")
        search_entry.pack(pady=5)

        def search_user():
            username = search_entry.get()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

            if user:
                ctk.CTkLabel(self, text=f"User Found: {username}").pack(pady=5)
            else:
                ctk.CTkLabel(self, text="User not found.").pack(pady=5)

        ctk.CTkButton(self, text="Search", command=search_user).pack(pady=10)

    def add_climb_page(self):
        for widget in self.winfo_children():
            if widget != self.bottom_nav:
                widget.destroy()

        ctk.CTkLabel(self, text="Add Climb").pack(pady=10)

        grade_entry = ctk.CTkEntry(self, placeholder_text="Grade")
        grade_entry.pack(pady=5)

        moves_entry = ctk.CTkEntry(self, placeholder_text="Number of Moves")
        moves_entry.pack(pady=5)

        def upload_file():
            file_path = Climbs.pick_file()
            ctk.CTkLabel(self, text=f"File Selected: {file_path}").pack(pady=5)
            return file_path

        ctk.CTkButton(self, text="Upload File", command=upload_file).pack(pady=10)

        def save_climb():
            grade = grade_entry.get()
            moves = moves_entry.get()
            file_path = upload_file()

            cursor.execute("INSERT INTO climbs (user_id, grade, moves, file_path) VALUES (?, ?, ?, ?)",
                           (self.username, grade, moves, file_path))
            connection.commit()
            ctk.CTkLabel(self, text="Climb added successfully.").pack(pady=10)

        ctk.CTkButton(self, text="Save Climb", command=save_climb).pack(pady=10)

    def open_file(self, file_path):
        if os.path.exists(file_path):
            os.startfile(file_path)
        else:
            ctk.CTkLabel(self, text="File not found.").pack(pady=10)

if __name__ == "__main__":
    app = WrappedRock()
    app.mainloop()

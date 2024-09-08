import mysql.connector
import tkinter as tk
import random
import datetime

from PIL import Image, ImageTk
from tkinter import messagebox, ttk

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
        self.root.geometry("1200x800")
        self.root.resizable(0,0)
        self.current_user_account_type = None
        self.login_form()

    def login_form(self):
        self.clear_frame()
        self.root.config(bg="#f0f0f0")

        # Open and resize the image
        original_image = Image.open("image/cmi.jpg")
        resized_image = original_image.resize((1200, 800))
        img = ImageTk.PhotoImage(resized_image)

        # Display the resized image
        panel = tk.Label(self.root, image=img)
        panel.image = img
        panel.pack(side="bottom", fill="both", expand="yes")


        self.login_frame = tk.Frame(self.root, bg="light gray", borderwidth=2, relief="groove", highlightbackground="black", highlightthickness=2, bd=10)
        self.login_frame.place(relx=0.5, rely=0.3, anchor=tk.CENTER,  relwidth=0.2, relheight=0.3)
  
        tk.Label(self.login_frame, text="Log in", font=("Helvetica", 24, "bold"), bg="light gray").pack()

        tk.Label(self.login_frame, text="Username:").pack()
        self.entry_username = tk.Entry(self.login_frame)
        self.entry_username.pack()

        tk.Label(self.login_frame, text="Password:").pack()
        self.entry_password = tk.Entry(self.login_frame, show="*")
        self.entry_password.pack()

        login = tk.Button(self.login_frame, text="Login", bg="light blue", command=self.authenticate_user)
        login.pack(pady=(10, 0))
        create = tk.Button(self.login_frame, text="Create Account", bg="light blue", command=self.create_user_form)
        create.pack(pady=(10, 0))
  
        self.root.config(bg="light gray")


    def authenticate_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if not username or not password:
            messagebox.showerror("Error", "Username and password fields cannot be empty.")
            return
        user = self.db.query("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))

        if user:
            if user[0][3] == 'Admin':
                self.current_user_account_type = 'Admin'
                messagebox.showinfo("Success", "Authentication successful!")
                self.clear_frame()
                AdminDashboard(self.root, self.db)
            else:
                self.current_user_account_type = 'User'
                messagebox.showinfo("Success", "Authentication successful!")
                ExamFunctions(self.root, self.db, user[0][0]).start_exam()
        else:
            messagebox.showerror("Error", "Invalid username or password. Please try again.")

    def create_user_form(self):
        self.clear_frame()
        self.create_user_frame = tk.Frame(self.root, bg="light gray")
        self.create_user_frame.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        tk.Label(self.create_user_frame, text="Create Account", font=("Helvetica", 24, "bold"), bg="light gray").pack()
        fields = ["Username", "Password", "Account Type", "First Name", "Middle Name", "Last Name"]
        self.user_entries = {}
        

        for field in fields:
            tk.Label(self.create_user_frame, text=field + ":").pack()
            if field == "Account Type":
                account_types = ["Admin", "User"] if self.current_user_account_type == "Admin" else ["User"]
                self.account_type_var = tk.StringVar(self.create_user_frame)
                self.account_type_var.set("User")
                ttk.Combobox(self.create_user_frame, textvariable=self.account_type_var, values=account_types, state="readonly").pack()
                self.user_entries[field] = self.account_type_var
            else:
                entry = tk.Entry(self.create_user_frame)
                entry.pack()
                self.user_entries[field] = entry

        submit = tk.Button(self.create_user_frame, text="Submit", bg="light blue", command=self.submit_user)
        submit.pack(pady =(10,0))
        login = tk.Button(self.create_user_frame, text="Login", bg="light blue", command=self.login_form)
        login.pack(pady =(10,0))

    def submit_user(self):
        data = [entry.get() for entry in self.user_entries.values()]
        username = data[0]

        existing_user = self.db.query("SELECT * FROM users WHERE username = %s", (username,))
        if not existing_user:
            try:
                self.db.execute("INSERT INTO users (username, password, account_type, first_name, middle_name, last_name) VALUES (%s, %s, %s, %s, %s, %s)", tuple(data))
                messagebox.showinfo("Success", "User account created successfully!")
                self.login_form()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error creating user account: {err}")
        else:
            messagebox.showerror("Error", "Username already exists. Please choose a different username.")

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class ExamFunctions:
    def __init__(self, root, db, user_id):
        self.root = root
        self.db = db
        self.user_id = user_id
        self.questions = []
        self.current_question_index = 0
        self.course_name = ""
        self.load_questions()

    def merge_sort(self, arr):
        if len(arr) > 1:
            mid = len(arr) // 2
            Left = arr[:mid]
            Right = arr[mid:]

            self.merge_sort(Left)
            self.merge_sort(Right)

            i = j = k = 0

            while i < len(Left) and j < len(Right):
                if Left[i][3] < Right[j][3]:
                    arr[k] = Left[i]
                    i += 1
                else:
                    arr[k] = Right[j]
                    j += 1
                k += 1

            while i < len(Left):
                arr[k] = Left[i]
                i += 1
                k += 1

            while j < len(Right):
                arr[k] = Right[j]
                j += 1
                k += 1

    def load_questions(self):
        self.questions = self.db.query("SELECT q.question_id, q.course_id, q.question, c.course_name FROM questions q JOIN courses c ON q.course_id = c.course_id")
        random.shuffle(self.questions)
        self.merge_sort(self.questions)
    def start_exam(self):
        
        self.show_question()

    def show_question(self):
        self.clear_frame()
        if self.current_question_index < len(self.questions):
            current_question = self.questions[self.current_question_index]
            self.course_name = current_question[3]

            label_course_name = tk.Label(self.root, text=f"Course name: {self.course_name}", font=("Helvetica", 20, "bold"), fg="red", bg="light grey")
            label_course_name.pack(pady=(50, 10))
            label_question_number = tk.Label(self.root, text=f"Question {self.current_question_index + 1} / {len(self.questions)}:", font=("Helvetica", 16, "bold"), bg="light grey")
            label_question_number.pack(pady=(50, 10))
            label_current = tk.Label(self.root, text=current_question[2], font=("Helvetica", 16, "bold"))
            label_current.pack()

            slide = tk.Scale(self.root, from_=0, to=10, orient="horizontal", length=400, bg="light grey")
            slide.pack(pady=(50, 10))

            button_next = tk.Button(self.root, text="Next", bg="light blue", width=18, height=2, command=lambda: self.answer_and_next_question(current_question[0], slide.get()))
            button_next.pack(pady=(20, 0))
        else:
            messagebox.showinfo("End of Exam", "You have reached the end of the exam.")
            ResultFunctions(self.root, self.db, self.user_id).recommend_course()

    def answer_and_next_question(self, question_id, answer_value):
        self.db.execute("INSERT INTO answer_log (user_id, question_id, answer_value, course_name) VALUES (%s, %s, %s, %s)",
                        (self.user_id, question_id, answer_value, self.course_name))
        self.current_question_index += 1
        self.show_question()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class ResultFunctions:
    def __init__(self, root, db, user_id):
        self.root = root
        self.db = db
        self.user_id = user_id

    def calculate_course_suitability(self):
        total_sum_weighted_scores = 0
        course_scores = {}
        total_scores = self.db.query("SELECT course_name, SUM(answer_value) as total_score FROM answer_log WHERE user_id = %s GROUP BY course_name", (self.user_id,))
        for total in total_scores:
            course_scores[total[0]] = total[1]
            total_sum_weighted_scores += total[1]

        for course in course_scores:
            course_scores[course] = (course_scores[course] / total_sum_weighted_scores) * 100
        return course_scores

    def recommend_course(self):
        self.clear_frame()
        results_frame = tk.Frame(self.root, bg="light grey")
        results_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        label_results = tk.Label(results_frame, text="Recommended Courses:", font=("Helvetica", 24, "bold"), bg="light grey")
        label_results.pack(pady=(10, 20))

        course_scores = self.calculate_course_suitability()
        sorted_courses = sorted(course_scores.items(), key=lambda x: x[1], reverse=True)
        for course, score in sorted_courses:
            tk.Label(results_frame, text=f"{course}: {score:.2f}%", font=("Helvetica", 16), bg="light grey").pack()

        button_exit = tk.Button(results_frame, text="Exit", bg="light blue", command=self.root.quit)
        button_exit.pack(pady=(20, 10))

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class AdminDashboard:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.admin_dashboard()

    def admin_dashboard(self):
        self.clear_frame()
        self.root.config(bg="light grey")
        dashboard_frame = tk.Frame(self.root, bg="light grey")
        dashboard_frame.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        
        tk.Label(dashboard_frame, text="Admin Dashboard", font=("Helvetica", 24, "bold"), bg="light grey").pack(pady=(10, 10))

        tk.Button(dashboard_frame, text="Create Questions", bg="light blue", command=self.create_question_form).pack(pady=(10, 0))
        tk.Button(dashboard_frame, text="Create Course", bg="light blue", command=self.create_course_form).pack(pady=(10, 0))
        tk.Button(dashboard_frame, text="User Reports", bg="light blue", command=self.generate_user_reports).pack(pady=(10, 0))
        tk.Button(dashboard_frame, text="Log Out", bg="light blue", command=self.logout).pack(pady=(10, 0))
        
        self.root.config(bg="light grey")

    def create_question_form(self):
        self.clear_frame()
        question_frame = tk.Frame(self.root, bg="light grey")
        question_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        tk.Label(question_frame, text="Create Question", font=("Helvetica", 24, "bold"), bg="light grey").pack(pady=(10, 10))

        courses = self.db.query("SELECT course_id, course_name FROM courses")
        self.course_var = tk.StringVar(question_frame)
        self.course_var.set("Select Course")
        course_dropdown = ttk.Combobox(question_frame, textvariable=self.course_var, values=[course[1] for course in courses], state="readonly")
        course_dropdown.pack(pady=(10, 10))

        self.question_entry = tk.Entry(question_frame, width=50)
        self.question_entry.pack(pady=(10, 10))

        tk.Button(question_frame, text="Submit", bg="light blue", command=self.submit_question).pack(pady=(10, 10))
        tk.Button(question_frame, text="Back to Dashboard", bg="light blue", command=self.admin_dashboard).pack(pady=(10, 10))

    def submit_question(self):
        course_name = self.course_var.get()
        question_text = self.question_entry.get()

        if course_name == "Select Course" or not question_text:
            messagebox.showerror("Error", "Please select a course and enter a question.")
            return

        course_id = self.db.query("SELECT course_id FROM courses WHERE course_name = %s", (course_name,))[0][0]
        self.db.execute("INSERT INTO questions (course_id, question) VALUES (%s, %s)", (course_id, question_text))
        messagebox.showinfo("Success", "Question created successfully.")
        self.admin_dashboard()

    def create_course_form(self):
        self.clear_frame()
        course_frame = tk.Frame(self.root, bg="light grey")
        course_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(course_frame, text="Create Course", font=("Helvetica", 24, "bold"), bg="light grey").pack(pady=(10, 10))

        self.course_name_entry = tk.Entry(course_frame, width=50)
        self.course_name_entry.pack(pady=(10, 10))

        tk.Button(course_frame, text="Submit", bg="light blue", command=self.submit_course).pack(pady=(10, 10))
        tk.Button(course_frame, text="Back to Dashboard", bg="light blue", command=self.admin_dashboard).pack(pady=(10, 10))

    def submit_course(self):
        course_name = self.course_name_entry.get()

        if not course_name:
            messagebox.showerror("Error", "Please enter a course name.")
            return

        self.db.execute("INSERT INTO courses (course_name) VALUES (%s)", (course_name,))
        messagebox.showinfo("Success", "Course created successfully.")
        self.admin_dashboard()

    def generate_user_reports(self):
        self.clear_frame()
        report_frame = tk.Frame(self.root, bg="light grey")
        report_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(report_frame, text="User Reports", font=("Helvetica", 24, "bold"), bg="light grey").pack(pady=(10, 10))

        user_ids = self.db.query("SELECT DISTINCT user_id FROM answer_log")
        for user in user_ids:
            user_id = user[0]
            user_info = self.db.query("SELECT username, first_name, last_name FROM users WHERE user_id = %s", (user_id,))
            username, first_name, last_name = user_info[0]
            tk.Label(report_frame, text=f"User: {username} ({first_name} {last_name})", font=("Helvetica", 16), bg="light grey").pack(pady=(5, 5))

            user_scores = self.db.query("SELECT course_name, SUM(answer_value) as total_score FROM answer_log WHERE user_id = %s GROUP BY course_name", (user_id,))
            for score in user_scores:
                tk.Label(report_frame, text=f"{score[0]}: {score[1]}", font=("Helvetica", 14), bg="light grey").pack(pady=(2, 2))

        tk.Button(report_frame, text="Back to Dashboard", bg="light blue", command=self.admin_dashboard).pack(pady=(10, 10))

    def logout(self):
        self.clear_frame()
        LoginPage(self.root, self.db)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    db = Database()
    root = tk.Tk()
    LoginPage(root, db)
    root.mainloop()

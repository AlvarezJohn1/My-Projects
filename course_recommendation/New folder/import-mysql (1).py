import mysql.connector
import tkinter as tk
import random
import datetime
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
		self.root.geometry("900x600")
		self.current_user_account_type = None
		self.login_form()

	def login_form(self):
		self.clear_frame()
		self.login_frame = tk.Frame(self.root, bg="light gray")
		self.login_frame.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
  
		tk.Label(self.login_frame, text="Log in", font=("Helvetica", 24, "bold"), bg="light gray").pack()

		tk.Label(self.login_frame, text="Username:").pack()
		self.entry_username = tk.Entry(self.login_frame)
		self.entry_username.pack()

		tk.Label(self.login_frame, text="Password:").pack()
		self.entry_password = tk.Entry(self.login_frame, show="*")
		self.entry_password.pack()

		tk.Button(self.login_frame, text="Login", bg="light blue", command=self.authenticate_user).pack()
		tk.Button(self.login_frame, text="Create Account", bg="light blue", command=self.create_user_form).pack()
  
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

		tk.Button(self.create_user_frame, text="Submit", bg="light blue", command=self.submit_user).pack()
		tk.Button(self.create_user_frame, text="Login", bg="light blue", command=self.login_form).pack()

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

	def load_questions(self):
		self.questions = self.db.query("SELECT q.question_id, q.course_id, q.question, c.course_name FROM questions q JOIN courses c ON q.course_id = c.course_id")
		random.shuffle(self.questions)

	def start_exam(self):
		
		self.show_question()

	def show_question(self):
		self.clear_frame()
		if self.current_question_index < len(self.questions):
			current_question = self.questions[self.current_question_index]
			self.course_name = current_question[3]

			tk.Label(self.root, text=f"Course name: {self.course_name}", font=("Helvetica", 16, "bold"), fg="red", bg="light grey").pack()
			tk.Label(self.root, text=f"Question {self.current_question_index + 1} / {len(self.questions)}:", font=("Helvetica", 14, "bold"),bg="light grey").pack() 
			tk.Label(self.root, text=current_question[2]).pack() 

			slide = tk.Scale(self.root, from_=0, to=10, orient="horizontal", length=250, bg="light grey")
			slide.pack()

			tk.Button(self.root, text="Next", bg = "light blue",command=lambda: self.answer_and_next_question(current_question[0], slide.get())).pack()
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

	def recommend_course(self):
		self.clear_frame()
		user_info = self.db.query("SELECT first_name FROM users WHERE user_id = %s", (self.user_id,))

		if user_info:
			first_name = user_info[0][0]
		else:
			first_name = "User"
		results = self.db.query("SELECT course_name, SUM(answer_value) FROM answer_log WHERE user_id = %s GROUP BY course_name", (self.user_id,))

		total_score = sum(score for course, score in results)
		max_possible_score = len(results) * 10  
		
		# Calculate percentages for each course
		course_percentages = [(course, (score / max_possible_score) * 100) for course, score in results]

		# Sort courses based on percentage
		course_percentages.sort(key=lambda x: x[1], reverse=True)

		# Display recommendations and percentages
		recommendation_text = f"{first_name}, here are the course recommendations based on your preferences:\n"
		for course, percentage in course_percentages:
			recommendation_text += f"{course}: {percentage:.2f}%\n"

		recommendation_label = tk.Label(self.root, text=recommendation_text)
		recommendation_label.pack(anchor="center", pady=100)
			
		date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		self.db.execute("INSERT INTO result (user_id, course_name, date) VALUES (%s, %s, %s)",
						(self.user_id, course_percentages[0][0], date_now))
		tk.Button(self.root, text="Start Exam Again",bg="light blue", command=self.start_exam_again).pack() 
		tk.Button(self.root, text="Logout",bg="red", command=self.logout).pack() 
		self.delete_answer_log()

	def delete_answer_log(self):
		cursor = self.db.db.cursor()
		cursor.execute("DELETE FROM answer_log WHERE user_id = %s", (self.user_id,))
		self.db.db.commit()
		cursor.close()
			
	def start_exam_again(self):
	
		ExamFunctions(self.root, self.db, self.user_id).start_exam()

	def logout(self):
		self.root.destroy()
		root = tk.Tk()
		LoginPage(root, self.db)
		root.mainloop()
		
	def clear_frame(self):
		for widget in self.root.winfo_children():
			widget.pack_forget()



class AdminDashboard:
	def __init__(self, root, db):
		self.root = root
		self.db = db

		self.root.title("Admin Dashboard")
		self.root.geometry("900x600")
  
		self.root.config(bg="light gray")

		self.tab_control = ttk.Notebook(root)
		self.question_tab = ttk.Frame(self.tab_control)
		self.course_tab = ttk.Frame(self.tab_control)
		self.result_tab = ttk.Frame(self.tab_control)

		self.tab_control.add(self.question_tab, text="Questions")
		self.tab_control.add(self.course_tab, text="Courses")
		self.tab_control.add(self.result_tab, text="Results")
		self.tab_control.pack(expand=1, fill="both")

		self.create_question_tab()
		self.create_course_tab()
		self.create_result_tab()
# _________________________________________________________

	def create_question_tab(self):

		self.question_tree = ttk.Treeview(self.question_tab)
		self.question_tree["columns"] = ("ID", "Course", "Question")

		self.question_tree.column("#0", width=0, stretch=tk.NO)
		self.question_tree.column("ID", anchor=tk.CENTER, width=50)
		self.question_tree.column("Course", anchor=tk.W, width=50)
		self.question_tree.column("Question", anchor=tk.W, width=500)

		self.question_tree.heading("#0", text="", anchor=tk.W)
		self.question_tree.heading("ID", text="ID", anchor=tk.CENTER)
		self.question_tree.heading("Course", text="Course ID", anchor=tk.W)
		self.question_tree.heading("Question", text="Question", anchor=tk.W)
  
		self.question_tree.pack(expand=True, fill="both")

		tk.Button(self.question_tab, text="Add Question", command=self.add_question, bg="light blue").pack()
		tk.Button(self.question_tab, text="Delete Question", command=self.delete_question, bg="light blue").pack()

		logout_button = tk.Button(self.root, text="Logout", command=self.logout, fg="white", bg="red")
		logout_button.pack(side=tk.TOP, anchor=tk.NE)

		self.refresh_question()

	def create_course_tab(self):
		self.course_tree = ttk.Treeview(self.course_tab)
		self.course_tree["columns"] = ("ID", "Course")

		self.course_tree.column("#0", width=0, stretch=tk.NO)
		self.course_tree.column("ID", anchor=tk.CENTER, width=50)
		self.course_tree.column("Course", anchor=tk.W, width=500)

		self.course_tree.heading("#0", text="", anchor=tk.W)
		self.course_tree.heading("ID", text="ID", anchor=tk.CENTER)
		self.course_tree.heading("Course", text="Course", anchor=tk.W)

		self.course_tree.pack(expand=True, fill="both")
  
		tk.Button(self.course_tab, text="Add Course", command=self.add_course, bg="light blue").pack()
		tk.Button(self.course_tab, text="Delete Course", command=self.delete_course, bg="light blue").pack()

		self.refresh_course()
   
	def create_result_tab(self):
		
		self.result_tree = ttk.Treeview(self.result_tab)
		self.result_tree["columns"] = ("ID", "User ID", "Course", "Date")

		self.result_tree.column("#0", width=0, stretch=tk.NO)
		self.result_tree.column("ID", anchor=tk.CENTER, width=50)
		self.result_tree.column("User ID", anchor=tk.CENTER, width=100)
		self.result_tree.column("Course", anchor=tk.W, width=300)
		self.result_tree.column("Date", anchor=tk.CENTER, width=150)

		self.result_tree.heading("#0", text="", anchor=tk.W)
		self.result_tree.heading("ID", text="ID", anchor=tk.CENTER)
		self.result_tree.heading("User ID", text="User ID", anchor=tk.CENTER)
		self.result_tree.heading("Course", text="Course Name", anchor=tk.W)
		self.result_tree.heading("Date", text="Date", anchor=tk.CENTER)

		self.result_tree.pack(expand=True, fill="both")
  
		# tk.Button(self.result_tab, text="View Results", command=self.view_results).pack()

		self.refresh_result()

# _________________________________________________________

	def add_question(self):
		add_question_window = tk.Toplevel(self.root)
		add_question_window.title("Add Question")
		add_question_window.geometry("400x200")

		tk.Label(add_question_window, text="Question:").pack()
		question_entry = tk.Entry(add_question_window, width=50)
		question_entry.pack()

		tk.Label(add_question_window, text="Course ID:").pack()
		course_id_entry = tk.Entry(add_question_window, width=50)
		course_id_entry.pack()
		
		def add_question_to_db():
			question_text = question_entry.get()
			course_id = course_id_entry.get()

			if question_text and course_id:
				try:
					self.db.execute("INSERT INTO questions (question, course_id) VALUES (%s, %s)", (question_text, course_id))
					messagebox.showinfo("Success", "Question added successfully!")
					self.refresh_question()
					add_question_window.destroy()
				except Exception as e:
					messagebox.showerror("Error", f"Failed to add question: {e}")
			else:
				messagebox.showerror("Error", "Please fill in all fields.")

		tk.Button(add_question_window, text="Add Question", command=add_question_to_db).pack()
  
		self.refresh_question()

	def delete_question(self):
		delete_question_window = tk.Toplevel(self.root)
		delete_question_window.title("Delete Question")
		delete_question_window.geometry("400x150")

		tk.Label(delete_question_window, text="Question ID:").pack()
		question_id_entry = tk.Entry(delete_question_window, width=50)
		question_id_entry.pack()

		def delete_question_from_db():
			question_id = question_id_entry.get()

			if question_id:
				try:
					self.db.execute("DELETE FROM questions WHERE question_id = %s", (question_id,))
					messagebox.showinfo("Success", "Question deleted successfully!")
					self.refresh_question()
					delete_question_window.destroy()
				except Exception as e:
					messagebox.showerror("Error", f"Failed to delete question: {e}")
			else:
				messagebox.showerror("Error", "Please enter the question ID.")

		tk.Button(delete_question_window, text="Delete Question", command=delete_question_from_db).pack()
		self.refresh_question()

	def add_course(self):
		add_course_window = tk.Toplevel(self.root)
		add_course_window.title("Add Course")
		add_course_window.geometry("400x150")

		tk.Label(add_course_window, text="Course Name:").pack()
		course_name_entry = tk.Entry(add_course_window, width=50)
		course_name_entry.pack()

		def add_course_to_db():
			course_name = course_name_entry.get()

			if course_name:
				try:
					self.db.execute("INSERT INTO courses (course_name) VALUES (%s)", (course_name,))
					messagebox.showinfo("Success", "Course added successfully!")
					self.refresh_course()
					add_course_window.destroy()
				except Exception as e:
					messagebox.showerror("Error", f"Failed to add course: {e}")
			else:
				messagebox.showerror("Error", "Please enter the course name.")
		tk.Button(add_course_window, text="Add Course", command=add_course_to_db).pack()
		self.refresh_course()

	def delete_course(self):

		delete_course_window = tk.Toplevel(self.root)
		delete_course_window.title("Delete Course")
		delete_course_window.geometry("400x150")

		tk.Label(delete_course_window, text="Course ID:").pack()
		course_id_entry = tk.Entry(delete_course_window, width=50)
		course_id_entry.pack()

		def delete_course_from_db():
			course_id = course_id_entry.get()

			if course_id:
				try:
					self.db.execute("DELETE FROM courses WHERE course_id = %s", (course_id,))
					messagebox.showinfo("Success", "Course deleted successfully!")
					self.refresh_course()
					delete_course_window.destroy()
				except Exception as e:
					messagebox.showerror("Error", f"Failed to delete course: {e}")
			else:
				messagebox.showerror("Error", "Please enter the course ID.")

		tk.Button(delete_course_window, text="Delete Course", command=delete_course_from_db).pack()
		self.refresh_course()

	def view_results(self):
		# view_results_window = tk.Toplevel(self.root)
		# view_results_window.title("View Results")
		# view_results_window.geometry("600x400")

		# results = self.db.query("SELECT * FROM result")	
		# results_listbox = tk.Listbox(view_results_window, width=100)
		# results_listbox.pack()

		# for result in results:
		# 	results_listbox.insert(tk.END, f"User ID: {result[0]}, Course Name: {result[1]}, Date: {result[2]}")

		# scrollbar = tk.Scrollbar(view_results_window, orient="vertical")
		# scrollbar.config(command=results_listbox.yview)
		# scrollbar.pack(side="right", fill="y")
		# results_listbox.config(yscrollcommand=scrollbar.set)
		# self.refresh_result()
		pass
  
# _________________________________________________________

	def refresh_question(self):
		for item in self.question_tree.get_children():
			self.question_tree.delete(item)
		questions = self.db.query("SELECT * FROM questions")
		for question in questions:
			self.question_tree.insert("", tk.END, values=question)
	 
	def refresh_course(self):
		for item in self.course_tree.get_children():
			self.course_tree.delete(item)
		courses = self.db.query("SELECT * FROM courses")
		for course in courses:
			self.course_tree.insert("", tk.END, values=course)
		
	def refresh_result(self):
		
		for item in self.result_tree.get_children():
			self.result_tree.delete(item)
		results = self.db.query("SELECT * FROM result")
		for result in results:
			self.result_tree.insert("", tk.END, values=result)
   
# _________________________________________________________
	 
	def logout(self):
		self.root.destroy()
		LoginPage(tk.Tk(), self.db)


if __name__ == "__main__":
	db = Database()
	root = tk.Tk()
	LoginPage(root, db)
	root.mainloop()
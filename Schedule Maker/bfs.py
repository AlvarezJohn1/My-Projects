import tkinter as tk
from tkinter import messagebox
from time import strftime
import json
import os
import pygame
from plyer import notification
from datetime import datetime

class ScheduleMaker:
    def __init__(self, root):
        self.root = root
        self.root.title("Schedule Maker")
        self.root.geometry("600x500")  # Increased size for date field

        # Set custom fonts and colors
        font_label = ("Century", 12, "bold")
        font_entry = ("Century", 10)
        font_button = ("Century", 10, "bold")
        bg_color = "#f0f8ff"  # Light blue background
        header_bg_color = "#4682B4"  # Steel blue background
        btn_color = "#4CAF50"
        btn_hover_color = "#45a049"
        btn_fg_color = "white"
        text_color = "#ffffff"

        self.root.configure(bg=bg_color)

        # Header Label with real-time clock
        self.header_frame = tk.Frame(root, bg=header_bg_color)
        self.header_frame.grid(row=0, column=0, columnspan=4, pady=10, padx=10, sticky="ew")
        self.time_label = tk.Label(self.header_frame, font=("Century", 16, "bold"), bg=header_bg_color, fg=text_color)
        self.time_label.pack(side=tk.RIGHT, padx=10)
        tk.Label(self.header_frame, text="Weekly Schedule Maker", font=("Century", 16, "bold"), bg=header_bg_color, fg=text_color).pack(side=tk.LEFT, padx=10)

        # Labels
        tk.Label(root, text="Task", font=font_label, bg=bg_color).grid(row=1, column=0, padx=10, pady=10)
        tk.Label(root, text="Date", font=font_label, bg=bg_color).grid(row=1, column=1, padx=10, pady=10)
        tk.Label(root, text="Day", font=font_label, bg=bg_color).grid(row=1, column=2, padx=10, pady=10)
        tk.Label(root, text="Start Time", font=font_label, bg=bg_color).grid(row=1, column=3, padx=10, pady=10)
        tk.Label(root, text="End Time", font=font_label, bg=bg_color).grid(row=1, column=4, padx=10, pady=10)

        # Entry widgets for task, date, start time, and end time
        self.task_entry = tk.Entry(root, font=font_entry)
        self.task_entry.grid(row=2, column=0, padx=10, pady=10)

        self.date_entry = tk.Entry(root, font=font_entry)
        self.date_entry.grid(row=2, column=1, padx=10, pady=10)
        tk.Label(root, text="YYYY-MM-DD", font=("Century", 8), bg=bg_color).grid(row=3, column=1, padx=10, pady=0)

        # Dropdown for day selection
        self.day_var = tk.StringVar(value="Monday")
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.day_menu = tk.OptionMenu(root, self.day_var, *days_of_week)
        self.day_menu.config(font=font_entry)
        self.day_menu.grid(row=2, column=2, padx=10, pady=10)

        self.start_time_entry = tk.Entry(root, font=font_entry)
        self.start_time_entry.grid(row=2, column=3, padx=10, pady=10)

        self.end_time_entry = tk.Entry(root, font=font_entry)
        self.end_time_entry.grid(row=2, column=4, padx=10, pady=10)

        # Buttons for adding task and showing schedule
        add_task_btn = tk.Button(root, text="Add Task", font=font_button, bg=btn_color, fg=btn_fg_color, command=self.add_task)
        add_task_btn.grid(row=3, column=0, columnspan=2, pady=20, padx=10)

        show_schedule_btn = tk.Button(root, text="Show Schedule", font=font_button, bg=btn_color, fg=btn_fg_color, command=self.show_schedule)
        show_schedule_btn.grid(row=3, column=2, columnspan=3, pady=20, padx=10)

        # Add hover effect for buttons
        add_task_btn.bind("<Enter>", lambda e: add_task_btn.config(bg=btn_hover_color))
        add_task_btn.bind("<Leave>", lambda e: add_task_btn.config(bg=btn_color))
        show_schedule_btn.bind("<Enter>", lambda e: show_schedule_btn.config(bg=btn_hover_color))
        show_schedule_btn.bind("<Leave>", lambda e: show_schedule_btn.config(bg=btn_color))

        # Initialize clock and schedule list
        self.schedule = []
        self.load_schedule()  # Load tasks from file
        self.update_time()

        # Initialize pygame mixer for sound
        pygame.mixer.init()
        self.notification_sound = pygame.mixer.Sound(r"C:\Users\johnd\OneDrive\Desktop\BFS\morning_alarm_2.mp3")  # Ensure you have this sound file in your directory

        # Check for task notification every minute
        self.check_notifications()

    def update_time(self):
        """Updates the time label to show the current time."""
        current_time = strftime("%H:%M:%S %p")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)  # Update time every second

    def add_task(self):
        task = self.task_entry.get()
        date = self.date_entry.get()
        day = self.day_var.get()
        start_time = self.start_time_entry.get()
        end_time = self.end_time_entry.get()

        if not task or not date or not start_time or not end_time:
            messagebox.showwarning("Input Error", "Please fill in all fields")
            return

        # Validate date format
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Date Error", "Please enter the date in YYYY-MM-DD format")
            return

        # Add task to the schedule list
        self.schedule.append({"task": task, "date": date, "day": day, "start": start_time, "end": end_time})

        # Save task to file
        self.save_schedule()

        # Clear input fields
        self.task_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.start_time_entry.delete(0, tk.END)
        self.end_time_entry.delete(0, tk.END)

    def show_schedule(self):
        schedule_window = tk.Toplevel(self.root)
        schedule_window.title("Your Schedule")
        schedule_window.geometry("500x400")
        schedule_window.configure(bg="#e7f3f3")

        # Display all tasks, grouped by date
        for task in self.schedule:
            task_text = f"{task['date']} ({task['day']}) {task['start']} - {task['end']}: {task['task']}"
            tk.Label(schedule_window, text=task_text, font=("Century", 12), bg="#e7f3f3").pack(pady=5)

    def save_schedule(self):
        """Save the current schedule to a JSON file."""
        with open("schedule.json", "w") as f:
            json.dump(self.schedule, f)

    def load_schedule(self):
        """Load the schedule from the JSON file if it exists."""
        if os.path.exists("schedule.json"):
            with open("schedule.json", "r") as f:
                self.schedule = json.load(f)

    def check_notifications(self):
        """Check if any task is due and display a notification."""
        current_time = strftime("%H:%M %p")
        current_date = strftime("%Y-%m-%d")

        for task in self.schedule:
            # Handle cases where 'date' key might be missing
            task_date = task.get("date", "")
            task_day = task.get("day", "")
            task_start_time = task.get("start", "")

            # If task date, day, and start time matches current date and time, show notification
            if task_date == current_date and task_day == strftime("%A") and task_start_time == current_time:
                # Play sound
                self.notification_sound.play()
                
                # Display system notification
                notification.notify(
                    title="Task Reminder",
                    message=f"It's time for: {task['task']}",
                    timeout=10  # Notification timeout in seconds
                )
                
        # Re-check every 60 seconds
        self.root.after(60000, self.check_notifications)

# Create the root window
root = tk.Tk()

# Instantiate the schedule maker
app = ScheduleMaker(root)

# Start the application
root.mainloop()

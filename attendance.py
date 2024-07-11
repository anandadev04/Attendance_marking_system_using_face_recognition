import customtkinter as ctk
from tkinter import simpledialog, messagebox
from pymongo import MongoClient
from datetime import datetime

# Function to connect to MongoDB
def connect_mongodb():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['attendance_db']
    attendance_collection = db['attendance']
    return attendance_collection

# Function to fetch students and attendance data
def fetch_data(date):
    attendance_collection = connect_mongodb()
    
    # Fetch all students and their attendance for the specified date
    attendance_records = list(attendance_collection.find({'date': date}))
    
    # Create a dictionary of attendance records
    attendance_dict = {record['name']: record for record in attendance_records}
    
    # Extract all students
    all_students = attendance_collection.distinct("name")
    
    return all_students, attendance_dict

# Function to fetch attendance data for a specific student
def fetch_student_attendance(student_name):
    attendance_collection = connect_mongodb()
    
    # Fetch attendance records for the specified student
    attendance_records = list(attendance_collection.find({'name': student_name}))
    
    attendance_dates = [record['date'] for record in attendance_records]
    
    return attendance_dates

# Function to display attendance
def display_attendance():
    date = date_entry.get()
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Error", "Incorrect date format. Please use YYYY-MM-DD.")
        return
    
    all_students, attendance_dict = fetch_data(date)
    
    for widget in result_frame.winfo_children():
        widget.destroy()
    
    for student_name in all_students:
        present = student_name in attendance_dict
        status = "✔" if present else "✘"
        
        row_frame = ctk.CTkFrame(result_frame)
        row_frame.pack(fill='x', padx=5, pady=2)
        
        name_label = ctk.CTkLabel(row_frame, text=student_name, anchor='w')
        name_label.pack(side='left', fill='x', expand=True)
        
        status_label = ctk.CTkLabel(row_frame, text=status, anchor='e')
        status_label.pack(side='right')
        
    result_frame.pack(fill='both', expand=True)

# Function to search attendance by student name
def search_attendance_by_name():
    student_name = simpledialog.askstring("Input", "Enter Student Name:")
    if not student_name:
        return
    
    attendance_dates = fetch_student_attendance(student_name)
    
    if not attendance_dates:
        messagebox.showinfo("Info", f"No attendance records found for {student_name}.")
        return
    
    attendance_collection = connect_mongodb()
    all_dates = attendance_collection.distinct("date")
    present_dates = set(attendance_dates)
    absent_dates = set(all_dates) - present_dates
    
    result_text = f"Attendance for {student_name}:\n\nPresent on:\n" + "\n".join(sorted(present_dates)) + "\n\nAbsent on:\n" + "\n".join(sorted(absent_dates))
    
    for widget in result_frame.winfo_children():
        widget.destroy()
    
    result_label = ctk.CTkLabel(result_frame, text=result_text, anchor='w', justify='left')
    result_label.pack(padx=5, pady=5)
    
    result_frame.pack(fill='both', expand=True)

# Function to go back to the main window
def go_back():
    root.destroy()
    main_window()

# Function to run the main window
def main_window():
    import main  # Assuming main.py contains the code for the main window

# Initialize the customtkinter library
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

# Create the main window
root = ctk.CTk()
root.title("Attendance Viewer")

# Set window size and position
root.geometry("550x450")
root.resizable(False, False)

# Create a frame for the date entry
date_frame = ctk.CTkFrame(root)
date_frame.pack(pady=10, padx=10, fill='x')

date_label = ctk.CTkLabel(date_frame, text="Enter Date (YYYY-MM-DD):")
date_label.pack(side='left')

date_entry = ctk.CTkEntry(date_frame)
date_entry.pack(side='left', padx=5, fill='x', expand=True)

fetch_button = ctk.CTkButton(date_frame, text="Fetch Attendance", command=display_attendance)
fetch_button.pack(side='left', padx=5)

# Create a frame for displaying the results
result_frame = ctk.CTkFrame(root)
result_frame.pack(pady=10, padx=10, fill='both', expand=True)

# Create a search button
search_button = ctk.CTkButton(root, text="Search Attendance by Name", command=search_attendance_by_name)
search_button.pack(pady=10)

# Create a back button
back_button = ctk.CTkButton(root, text="Back", command=go_back)
back_button.pack(pady=10)

# Run the customtkinter event loop
root.mainloop()

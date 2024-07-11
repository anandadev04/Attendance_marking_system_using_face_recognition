import customtkinter as ctk
from tkinter import simpledialog, messagebox
import subprocess
import json
import sys

def ask_name():
    name = simpledialog.askstring("Input", "What is your name?")
    if name:
        with open("username.json", "w") as file:
            json.dump({"name": name}, file)
        # Call the face_taker.py script
        python_executable = sys.executable  # This gets the path to the current Python interpreter
        subprocess.Popen([python_executable, "face_taker.py"])

def train_model():
    # Call the face_train.py script
    python_executable = sys.executable  # This gets the path to the current Python interpreter
    process = subprocess.Popen([python_executable, "face_train.py"])
    process.wait()  # Wait for the process to complete
    messagebox.showinfo("Info", "Training Successful")

def recognize_faces():
    # Call the face_recognizer.py script
    python_executable = sys.executable  # This gets the path to the current Python interpreter
    subprocess.Popen([python_executable, "face_recognizer.py"])

def check_attendance():
    # Call the attendance_viewer.py script
    python_executable = sys.executable  # This gets the path to the current Python interpreter
    subprocess.Popen([python_executable, "attendance.py"])

# Initialize the customtkinter library
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

# Create the main window
root = ctk.CTk()
root.title("Face Recognition System")

# Set window size and position
root.geometry("400x300")
root.resizable(False, False)

# Create a frame for better layout
frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Create a label
label = ctk.CTkLabel(frame, text="Face Recognition System", font=ctk.CTkFont(size=20, weight="bold"))
label.pack(pady=20)

# Create a button that will call the ask_name function when pressed
enter_name_button = ctk.CTkButton(frame, text="Enter Name", command=ask_name)
enter_name_button.pack(pady=10)

# Create a button that will call the train_model function when pressed
train_model_button = ctk.CTkButton(frame, text="Train Model", command=train_model)
train_model_button.pack(pady=10)

# Create a button that will call the recognize_faces function when pressed
recognize_faces_button = ctk.CTkButton(frame, text="Recognize Faces", command=recognize_faces)
recognize_faces_button.pack(pady=10)

# Create a button that will call the check_attendance function when pressed
check_attendance_button = ctk.CTkButton(frame, text="Check Attendance", command=check_attendance)
check_attendance_button.pack(pady=10)

# Run the customtkinter event loop
root.mainloop()

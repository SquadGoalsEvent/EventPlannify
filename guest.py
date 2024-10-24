import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
# Include all the imports you've already used for the guest list functionality.
root = tk.Tk()
# Function to create the guest list window
def open_guest_list():
     subprocess.Popen(["python", "guestlist.py"]) # This function will create and display the guest list window
     root.destroy()  # Close the current dashboard window
     create_guest_list_window()  # Call the function to create the guest list window


def open_event_list():
     subprocess.Popen(["python", "Event2.py"]) # This function will create and display the guest list window
     root.destroy()  # Close the current dashboard window
     create_guest_list_window()  # Call the function to create the guest list window

def create_guest_list_window():
    # Copy your existing guest list code here, starting from creating the main window (root).
    # Ensure to use a different root window or modify as needed.

    # Create GUI
    guest_list_root = tk.Tk()
    guest_list_root.title("Guest List System")
    guest_list_root.geometry("1500x800")
    
    # Include the rest of your guest list code...
    # Make sure to replace any `root` references with `guest_list_root`.

# Function to create the dashboard window
def create_dashboard():
    dashboard = tk.Tk()
    dashboard.title("Dashboard")
    dashboard.geometry("600x400")

    welcome_label = tk.Label(dashboard, text="Welcome to the Dashboard", font=("Arial", 20))
    welcome_label.pack(pady=20)

    # Button to open the guest list
    guest_list_button = tk.Button(dashboard, text="GUESTS", command=open_guest_list, bg="#800080", fg="white", font=("Microsoft YaHei UI Light", 16))
    guest_list_button.pack(pady=10)

        # Button to open the guest list
    guest_list_button = tk.Button(dashboard, text="EVENTS", command=open_event_list, bg="#800080", fg="white", font=("Microsoft YaHei UI Light", 16))
    guest_list_button.pack(pady=10)

    # You can add more buttons for additional features as needed

    dashboard.mainloop()

# Start the application by creating the dashboard
create_dashboard()
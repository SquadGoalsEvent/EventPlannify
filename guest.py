import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Ensure you have Pillow installed
import subprocess

# Function to create the guest list window
def open_guest_list():
    subprocess.Popen(["python", "guestlist.py"])  # Opens guest list script
    root.destroy()  # Close the current dashboard window

def open_event_list():
    subprocess.Popen(["python", "Event2.py"])  # Opens event list script
    root.destroy()  # Close the current dashboard window

def create_dashboard():
    global root
    root = tk.Tk()
    root.title("Dashboard")
    root.geometry("1400x800")
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")

    # Load and set the background image
    bg_image = Image.open("pexels-abbykihano-431722.jpg")  # Update this path
    bg_image = bg_image.resize((1400, 800), Image.LANCZOS)  # Resize to fit the window
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Create a Canvas and set the background image
    canvas = tk.Canvas(root, width=1400, height=800)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Create a frame for the buttons to overlay on the background
    button_frame = tk.Frame(root, bg="white", bd=15, width=400, height=300)  # Set desired width and height
    button_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the button frame

    welcome_label = tk.Label(button_frame, text="Welcome to the Dashboard", font=("Arial", 20), bg="white")  # Set bg to white
    welcome_label.pack(pady=30)

    # Button to open the guest list
    guest_list_button = tk.Button(button_frame, text="GUESTS", command=open_guest_list, bg="#800080", fg="white", font=("Microsoft YaHei UI Light", 16))
    guest_list_button.pack(pady=15)

    # Button to open the event list
    event_list_button = tk.Button(button_frame, text="EVENTS", command=open_event_list, bg="#800080", fg="white", font=("Microsoft YaHei UI Light", 16))
    event_list_button.pack(pady=15)

    # Keep a reference to the image to prevent garbage collection
    canvas.bg_photo = bg_photo

    root.mainloop()

# Start the application by creating the dashboard
create_dashboard()



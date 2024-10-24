import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Ensure you have Pillow installed
import subprocess
import os 
from tkinter import Canvas
from tkinter import ttk

# Function to create the guest list window
def open_guest_list():
    subprocess.Popen(["python", "guestlist.py"])  # Opens guest list script
    root.destroy()  # Close the current dashboard window

def open_event_list():
    subprocess.Popen(["python", "Event2.py"])  # Opens event list script
    root.destroy()  # Close the current dashboard window

def create_text_with_outline(canvas, x, y, text, outline_color, text_color, font_size, font_weight ):
    for offset in range (-1, 2):
        for offset2 in range(-1,2):
            canvas.create_text(x + offset, y + offset2, text=text, fill = outline_color, font = ('Microsoft YaHei UI Light', font_size, font_weight), anchor = 'center')
        canvas.create_text(x, y, text = text, fill = text_color, font = ('Microsoft YaHei UI Light', font_size, font_weight), anchor = 'center')

def create_dashboard():
    global root
    root = tk.Tk()
    root.title("Dashboard")
    root.geometry("1400x800")
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")

    img_path = r'pexels-mikky-k-158844-625644.jpg'
    if os.path.exists(img_path):
        print("Image found.")
    img = Image.open(img_path)
    img_resized = img.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(img_resized)
        

    # Create a Canvas and set the background image
    canvas = tk.Canvas(root, width = root.winfo_screenwidth(), height = root.winfo_screenheight())
    
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    
    create_text_with_outline(canvas, root.winfo_screenwidth() // 2, root.winfo_screenheight() // 4, 
                             "Welcome to EventPlannify", "#888888", "#FFFFFF", 48, 'bold')
    create_text_with_outline(canvas, root.winfo_screenwidth() // 2, (root.winfo_screenheight() // 4) + 100, 
                             "Manage Your Events With Ease", "#000000", "#FFFFFF", 28, 'italic')


    button_style = {"font": ("Microsoft YaHei UI Light", 16), "bg": "#800080", "fg": "white", "activebackground": "#9933FF", "activeforeground": "white", "bd": 2, "relief": "groove", "width": 15, "height": 2}

    # Button to open the guest list
    guest_list_button = tk.Button(root, text="GUESTS", command=open_guest_list, bg="#800080", fg="white", font=("Microsoft YaHei UI Light", 16))
    canvas.create_window(root.winfo_screenwidth() //2, root.winfo_screenheight() // 2, anchor = "center", window = guest_list_button)

    # Button to open the event list
    event_list_button = tk.Button(root, text="EVENTS", command=open_event_list, bg="#800080", fg="white", font=("Microsoft YaHei UI Light", 16))
    canvas.create_window(root.winfo_screenwidth() // 2, (root.winfo_screenheight() // 2) + 60, anchor="center", window=event_list_button)
    
    
    # Keep a reference to the image to prevent garbage collection
    canvas.bg_photo = bg_photo

    root.mainloop()

# Start the application by creating the dashboard
create_dashboard()



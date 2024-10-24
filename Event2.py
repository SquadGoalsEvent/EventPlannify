
import tkinter as tk
from tkinter import Image, messagebox
from turtle import update
import PIL
import os
import json
import random
import string
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from tkinter import messagebox
from PIL import Image, ImageTk 
import requests

EVENTS_FILE = 'events.txt'


class Event:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Manager")
        self.root.geometry("1500x800")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")

    # app.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")

def load_background(main_content, image_path):

    if os.path.exists(image_path):
        bg_image = Image.open(image_path)
        bg_image = bg_image.resize((1200, 800), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Create a canvas and add the image to it
        canvas = tk.Canvas(main_content, width=600, height=400)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=bg_photo, anchor="nw")

        # Keep a reference to the image to prevent garbage collection
        canvas.bg_photo = bg_photo  # This line is crucial

        return canvas
    else:
        messagebox.showerror("Error", f"Image file not found: {image_path}")
        return None

<<<<<<< Updated upstream


def signin(username, password):
    # Add your login logic here
     with open('datasheet.txt', 'r') as file:
            username = file.readline().strip()  
        # if username and password:  # Simplified check
            welcome_label.config(text=f"Welcome, {username}")
        # display_events()  
=======
# def logout():
#     response = messagebox.askyesno("Logout", "Are you sure you want to logout?", font=('Microsoft YaHei UI Light', 20))
#     if response:
#         show_signin()
# Assuming welcome_label is defined globally or passed as an argument

>>>>>>> Stashed changes

def load_usernames():
    try:
        with open('usernames.txt', 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []

# def signin(username_entry, password_entry):
#     username = username_entry.get()
#     password = password_entry.get()

#     # Load usernames from the new file
#     usernames = load_usernames()

#     # You can use your existing logic for password verification, for example from 'datasheet.txt'
#     try:
#         with open('datasheet.txt', 'r') as file:
#             users = file.readlines()

#         for users in users[1]:
#             stored_username, stored_password = users.strip().split(',')
#             if username == stored_username and password == stored_password:
#                 if username in usernames:
#                     welcome_label.config(text=f"Welcome, {username}")
#                     display_events() 
#                 else:
#                     messagebox.showerror("Login Failed", "Username not found.")
#                 return

#         messagebox.showerror("Login Failed", "Invalid username or password.")

#     except FileNotFoundError:
#         messagebox.showerror("Error", "User data file not found.")
#     except Exception as e:
#         messagebox.showerror("Error", str(e))

# # def signin():
# #     # Read the username from the text file
# #     with open('events.txt', 'r') as file:
# #         username = file.readline().strip()  
# #         welcome_label.config(text=f"Welcome, {username}")    


def load_events():
    if os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, 'r') as file:
            events = file.readlines()
        return [event.strip() for event in events]
    return []

# Function to display the list of events on the dashboard
def display_events():

    for widget in main_content.winfo_children():
        widget.destroy()

    overlay_frame = load_background(main_content, "pexels-designecologist-2526105.png")
    if overlay_frame is None:
        return

    events = load_events()

    heading_label = tk.Label(overlay_frame, text="Event List", bg='black' ,font=("Microsoft YaHei UI Light", 20, "bold"), fg='white')
    heading_label.pack(anchor="center", pady=10)



  # Frame to hold the listbox and buttons
    listbox_frame = tk.Frame(overlay_frame, height=150, width=200)
    # listbox_frame.pack_propagate(False)
    listbox_frame.pack(fill="both", expand=True, padx=10, pady=10)

 

    # Scrollbar for the Listbox
    scrollbar = tk.Scrollbar(listbox_frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    # Listbox to display the list of events, with larger size
    global events_list
    events_list = tk.Listbox(listbox_frame, width=30, height=5, yscrollcommand=scrollbar.set)
    events_list.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=events_list.yview)
   

    if events:
        for event in events:
            events_list.insert(tk.END, event)
    else:
        events_list.insert(tk.END, "No events found.")

    button_frame = tk.Frame(overlay_frame, width=50)
    button_frame.pack(pady=10, padx=10, anchor="center" )

    edit_button = tk.Button(overlay_frame, text="Edit Event", command=edit_selected_event, bg="purple",fg='white', font=('Microsoft YaHei UI Light', 9 ))
    edit_button.pack(side="left", padx=10, pady=10, anchor='center')

    delete_button = tk.Button(overlay_frame, text="Delete Event",  command=delete_selected_event, bg="purple", fg='white',font=('Microsoft YaHei UI Light', 9 ) )
    delete_button.pack(side="left", padx=10, pady=10, anchor='center')


# Function to generate a random password
def generate_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

# Function to display the create event form
def show_create_event_form():
    # Clear the main content area
    for widget in main_content.winfo_children():
        widget.destroy()

    content_frame = tk.Frame(main_content)
    content_frame.pack(pady=20, padx=20, fill="x")

    # Label and Entry for Event Name
    event_name_label = tk.Label(main_content, text="Event Name:", bg="white", fg='Purple',font=('Microsoft YaHei UI Light', 15))
    event_name_label.pack(pady=10)
    event_name_entry = tk.Entry(main_content, width=30, 
                            highlightthickness=2, highlightbackground="#800080", highlightcolor="#800080")
    event_name_entry.pack(pady=5)

    event_date_label = tk.Label(main_content, text="Event Date:", bg="white", fg='Purple',font=('Microsoft YaHei UI Light', 15 ))
    event_date_label.pack(pady=10)
    event_date_entry = DateEntry(main_content, width=30, 
                              background='#800080', foreground='black',  
                              highlightthickness=2, highlightbackground="#800080", 
                              highlightcolor="#800080", borderwidth=2, 
                              date_pattern='y-mm-dd')
    event_date_entry.pack(pady=5)


 
    # Label and Entry for Event Location
    location_label = tk.Label(main_content, text="Location:", bg="white",fg='Purple',font=('Microsoft YaHei UI Light', 15 ) )
    location_label.pack(pady=10)
    location_entry = tk.Entry(main_content, width=30, 
                            highlightthickness=2, highlightbackground="#800080", highlightcolor="#800080")
    location_entry.pack(pady=5)

    # Label and Textbox for Event Description
    description_label = tk.Label(main_content, text="Description:", bg="white",fg='Purple',font=('Microsoft YaHei UI Light', 15 ) )
    description_label.pack(pady=10)
    description_entry = tk.Text(main_content, height=5, width=30, highlightthickness=2, highlightbackground="#800080", highlightcolor="#800080")
    description_entry.pack(pady=5)

    # Function to save the event
    def save_event():
        event_name = event_name_entry.get()
        event_date = event_date_entry.get_date()
        event_location = location_entry.get()
        event_description = description_entry.get("1.0", tk.END).strip()  
        password = generate_password()

        if event_name and event_date:
            # Save the event to the file with password
            with open(EVENTS_FILE, 'a') as file:
                file.write(f"{event_name} - {event_date} -{event_location} -  Description: {event_description} - Password: {password}\n")
            messagebox.showinfo("Success", f"Event created successfully!\nGenerated Password: {password}")
            display_events() 
        else:
            messagebox.showerror("Error", "Please fill in all fields!")

    button_frame = tk.Frame(content_frame)
    button_frame.grid(row=3, column=1, pady=10, padx=10, sticky="e")


    save_button = tk.Button(main_content, text="Save Event", command=save_event, bg="#800080", fg='white',font=('Microsoft YaHei UI Light', 9 ) )
    save_button.pack(side="left", padx=5, pady=5)


    cancel_button = tk.Button(main_content, text="Cancel", command=display_events, bg="#800080", fg='white',font=('Microsoft YaHei UI Light', 9 ) )
    cancel_button.pack(side="left", padx=5, pady=5)

# Function to delete an event
def delete_selected_event():
    selected_index = events_list.curselection()
    if selected_index:
        selected_event = events_list.get(selected_index)
        response = messagebox.askyesno("Delete Event", f"Are you sure you want to delete the event: {selected_event}?")
        if response:
            events = load_events()
            events.remove(selected_event)

            with open(EVENTS_FILE, 'w') as file:
                file.write("\n".join(events) + "\n")
            
            messagebox.showinfo("Success", "Event deleted successfully!")
            display_events()
    else:
        messagebox.showwarning("Warning", "Please select an event to delete.")
def edit_selected_event():
    selected_index = events_list.curselection()
    if selected_index:
        selected_event = events_list.get(selected_index)
        edit_selected_event_window(selected_event)
    else:
        messagebox.showwarning("Warning", "Please select an event to edit.")
def edit_selected_event_window(selected_event):
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Event")
    edit_window.geometry("1400x800")

    # Load and set the background image
    # bg_image = Image.open("EventPlannify/pexels-abbykihano-431722.jpg")  
    # bg_image = bg_image.resize((1400, 800), Image.LANCZOS) 
    # bg_photo = ImageTk.PhotoImage(bg_image)

    # # Create a label to hold the background image
    # bg_label = tk.Label(edit_window, image=bg_photo)
    # bg_label.image = bg_photo 
    # bg_label.place(x=0, y=0, relwidth=1, relheight=1)  
    event_parts = selected_event.split(" - ")
    event_name = event_parts[0]
    event_date = event_parts[1]
    event_description = event_parts[2]

    content_frame = tk.Frame(edit_window, highlightbackground="#800080", highlightthickness=2)
    content_frame.pack(expand=True, padx=10, pady=10)

    event_name_label = tk.Label(content_frame, text="Event Name:")
    event_name_label.pack(pady=10, anchor="center")
    event_name_entry = tk.Entry(content_frame, width=40)
    event_name_entry.pack(pady=5)
    event_name_entry.insert(0, event_name)

    event_date_label = tk.Label(content_frame, text="Event Date:")
    event_date_label.pack(pady=10, anchor="center")
    event_date_entry = DateEntry(content_frame, width=40, background='darkblue', 
                                 foreground='white', borderwidth=2, date_pattern='y-mm-dd')
    event_date_entry.pack(pady=5)
    event_date_entry.set_date(event_date)

    event_location_label = tk.Label(content_frame, text="Location:")
    event_location_label.pack(pady=10, anchor="center")
    event_location_entry = tk.Entry(content_frame, width=40)
    event_location_entry.pack(pady=5)
    event_location_entry.insert(0, event_name)

    description_label = tk.Label(content_frame, text="Description:")
    description_label.pack(pady=10, anchor="center")
    description_entry = tk.Text(content_frame, height=5, width=40)
    description_entry.pack(pady=5)
    description_entry.insert(tk.END, event_description)

    save_button = tk.Button(content_frame, text="Save Changes",fg="white", bg="#800080", command=lambda: save_edited_event(selected_event, event_name_entry, event_date_entry,event_location_entry, description_entry, edit_window))
    save_button.pack(pady=10, anchor="center")


def save_edited_event(selected_event, name_entry, date_entry, location_entry, description_entry, edit_window):
    new_event_name = name_entry.get()
    new_event_date = date_entry.get_date()
    new_event_location = location_entry.get()
    new_event_description = description_entry.get("1.0", tk.END).strip()
    password = generate_password()  # Ensure this is defined

    if new_event_name and new_event_date:
        new_event_details = f"{new_event_name} - {new_event_date} - {new_event_location} - {new_event_description} - Password: {password}\n"
        update_event_in_file(selected_event, new_event_details)
        messagebox.showinfo("Success", "Event updated successfully!")
        edit_window.destroy()
        display_events()  # Refresh the event list

def update_event_in_file(old_event, new_event):
    events = load_events()  # Ensure this loads your events correctly
    updated_events = [new_event if event == old_event else event for event in events]
    
    with open(EVENTS_FILE, 'w') as file:
        file.write("\n".join(updated_events) + "\n")


def guest_list():
    messagebox.showinfo("Guest List", "Guest List clicked!")
# Function to display the create guest form
def show_create_guest_form():
    # Clear the main content area
    for widget in main_content.winfo_children():
        widget.destroy()

    event_name_label = tk.Label(main_content, text="Guest Name:", bg="white", fg="black")
    event_name_label.pack(pady=10)
    event_name_entry = tk.Entry(main_content, width=30)
    event_name_entry.pack(pady=5)

def show_view_guest_list_form():
    messagebox.showinfo("View Guests, Guest have been view")




root = tk.Tk()
root.title("Dashboard")
root.geometry("1500x800")
root.config(bg="#d3d3d3") 

# Create the top frame
top_frame = tk.Frame(root, bg="#800080", height=50)
top_frame.place(relx=0.0, rely=0.0, relwidth=1, relheight=0.1)

<<<<<<< Updated upstream

=======
# Create the logout button
# logout_button = tk.Button(top_frame, text="Logout", command=logout, bg="#800080", fg="white")
# logout_button.pack(side="right", padx=10)
>>>>>>> Stashed changes

# Create the sidebar frame
sidebar_frame = tk.Frame(root, bg="#800080", width=150)
sidebar_frame.place(relx=0.0, rely=0.1, relheight=0.9, relwidth=0.25)

# Load and display the profile icon
# profile_icon = Image.open('user.png')  
# profile_icon = profile_icon.resize((50, 50), Image.LANCZOS) 
# profile_icon_tk = ImageTk.PhotoImage(profile_icon)

# icon_label = tk.Label(sidebar_frame, image=profile_icon_tk, bg="#800080")
# icon_label.pack(pady=10) 

# Create the welcome label under the icon
welcome_label = tk.Label(sidebar_frame, text="Event plannify", bg="#800080", fg="white", font=("Microsoft YaHei UI Light", 20))
welcome_label.pack(pady=25) 

# Load profile icon
<<<<<<< Updated upstream
img = Image.open("user.png")
resized_img = img.resize((50, 50), Image.LANCZOS)
photo_img = ImageTk.PhotoImage(resized_img)
root.profile_icon = photo_img
profile_icon_label = tk.Label(sidebar_frame, image=root.profile_icon, bg="#800080")
profile_icon_label.pack(pady=20)
=======
# img = Image.open("user.png")
# resized_img = img.resize((50, 50), Image.LANCZOS)
# photo_img = ImageTk.PhotoImage(resized_img)
# root.profile_icon = photo_img
# profile_icon_label = tk.Label(sidebar_frame, image=root.profile_icon, bg="#800080")
# profile_icon_label.pack(pady=20)
>>>>>>> Stashed changes


# Load icons for buttons
# Load icons for buttons
create_events_icon = Image.open("calendar (1).png")
create_events_icon = create_events_icon.resize((20, 20), Image.LANCZOS)
create_events_photo = ImageTk.PhotoImage(create_events_icon)

guest_list_icon = Image.open("guest-list.png")
guest_list_icon = guest_list_icon.resize((20, 20), Image.LANCZOS)
guest_list_photo = ImageTk.PhotoImage(guest_list_icon)

view_guest_icon = Image.open("target-audience.png")
view_guest_icon = view_guest_icon.resize((20, 20), Image.LANCZOS)
view_guest_photo = ImageTk.PhotoImage(view_guest_icon)

settings_icon = Image.open("cog.png")
settings_icon = settings_icon.resize((20, 20), Image.LANCZOS)
setting_photo = ImageTk.PhotoImage(view_guest_icon)

# Function to create a button with an icon and text
def create_button_with_icon(frame, text, command, icon):
    button = tk.Button(frame, text=text, command=command, bg="#800080", fg="white", font=("Microsoft YaHei UI Light", 20), image=icon, compound="left")
    button.pack(fill="x", pady=(15, 20))  

# Create buttons with icons
create_button_with_icon(sidebar_frame, "Create Events", show_create_event_form, create_events_photo)
create_button_with_icon(sidebar_frame, "Edit Events", show_create_guest_form, guest_list_photo)
create_button_with_icon(sidebar_frame, "Delete Events", show_view_guest_list_form, view_guest_photo)
create_button_with_icon(sidebar_frame, "View Event List", show_view_guest_list_form, view_guest_photo)
# create_button_with_icon(sidebar_frame, "settings",show_view_guest_list_form, setting_photo)


# create_events_button = tk.Button(sidebar_frame, text="Create Events", command=show_create_event_form, bg="#800080", fg="white") 
# create_events_button.pack(fill="x", pady=10)


# guest_list_button = tk.Button(sidebar_frame, text="Guest List", command=show_create_guest_form, bg="#800080", fg="white")  
# guest_list_button.pack(fill="x", pady=10)

# View_guest_button = tk.Button(sidebar_frame, text="View Guests", command= show_view_guest_list_form, bg="#800080", fg="white")
# View_guest_button.pack(fill="x", pady=10)


main_content = tk.Frame(root, bg="white")
main_content.place(relx=0.25, rely=0.1, relwidth=0.85, relheight=0.9)




display_events()
# signin()

root.mainloop()
import tkinter as tk
from tkinter import Image, messagebox
import PIL
from tkcalendar import Calendar, DateEntry
import os
import json
import random
import string
from PIL import Image, ImageTk

EVENTS_FILE = 'events.txt'


def logout():
    response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if response:
        root.quit()


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

    events = load_events()
    


    heading_label = tk.Label(main_content, text="Event List", bg="white", fg="#0000FF", font=("Arial", 16, "bold"))
    heading_label.pack(anchor="nw", padx=10, pady=10)

  # Frame to hold the listbox and buttons
    listbox_frame = tk.Frame(main_content, height=300, width=400)
    listbox_frame.pack_propagate(False)
    listbox_frame.pack(fill="both", expand=True, padx=10, pady=10)

 

    # Scrollbar for the Listbox
    scrollbar = tk.Scrollbar(listbox_frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    # Listbox to display the list of events, with larger size
    global events_list
    events_list = tk.Listbox(listbox_frame, width=50, height=15, yscrollcommand=scrollbar.set)
    events_list.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=events_list.yview)
   

    if events:
        for event in events:
            events_list.insert(tk.END, event)
    else:
        events_list.insert(tk.END, "No events found.")

    button_frame = tk.Frame(main_content, bg="white")
    button_frame.pack(pady=10, padx=10, anchor="e")

    edit_button = tk.Button(button_frame, text="Edit Event", command=edit_selected_event, bg="lightblue")
    edit_button.pack(side="right", padx=5)
    
    delete_button = tk.Button(button_frame, text="Delete Event", command=delete_selected_event, bg="red")
    delete_button.pack(side="right", padx=5)


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
    form_frame = tk.Frame(main_content, bg="pink")
    form_frame.pack(pady=20, padx=20, fill="x")

    # Label and Entry for Event Name
    event_name_label = tk.Label(main_content, text="Event Name:", bg="white", fg="black")
    event_name_label.pack(pady=10)
    event_name_entry = tk.Entry(main_content, width=30)
    event_name_entry.pack(pady=5)

    # Label and Calendar for Event Date
    event_date_label = tk.Label(main_content, text="Event Date:", bg="white", fg="black")
    event_date_label.pack(pady=10)

    event_date_entry = DateEntry(main_content, width=30, background='darkblue', 
                                 foreground='white', borderwidth=2, date_pattern='y-mm-dd')
    event_date_entry.pack(pady=5)

    # Label and Entry for Event Location
    location_label = tk.Label(main_content, text="Location:", bg="white", fg="black")
    location_label.pack(pady=10)
    location_entry = tk.Entry(main_content, width=30)
    location_entry.pack(pady=5)

    # Label and Textbox for Event Description
    description_label = tk.Label(main_content, text="Description:", bg="white", fg="black")
    description_label.pack(pady=10)
    description_entry = tk.Text(main_content, height=5, width=40)
    description_entry.pack(pady=5)

    # Function to save the event
    def save_event():
        event_name = event_name_entry.get()
        event_date = event_date_entry.get_date()  # Get the selected date from the DateEntry
        event_description = description_entry.get("1.0", tk.END).strip()  
        password = generate_password()

        if event_name and event_date:
            # Save the event to the file with password
            with open(EVENTS_FILE, 'a') as file:
                file.write(f"{event_name} - {event_date} - Description: {event_description} - Password: {password}\n")
            messagebox.showinfo("Success", f"Event created successfully!\nGenerated Password: {password}")
            display_events()  # Refresh the events list after saving
        else:
            messagebox.showerror("Error", "Please fill in all fields!")

    button_frame = tk.Frame(form_frame, bg="white")
    button_frame.grid(row=3, column=1, pady=10, padx=10, sticky="e")
  
    save_button = tk.Button(main_content, text="Save Event", command=save_event)
    save_button.pack(side="left", padx=5)


    cancel_button = tk.Button(main_content, text="Cancel", command=display_events)
    cancel_button.pack(side="left", padx=5)

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
    edit_window.geometry("400x300")

    event_parts = selected_event.split(" - ")
    event_name = event_parts[0]
    event_date = event_parts[1]
    event_description = event_parts[2]

    event_name_label = tk.Label(edit_window, text="Event Name:")
    event_name_label.pack(pady=10)
    event_name_entry = tk.Entry(edit_window, width=30)
    event_name_entry.pack(pady=5)
    event_name_entry.insert(0, event_name)

    event_date_label = tk.Label(edit_window, text="Event Date:")
    event_date_label.pack(pady=10)
    event_date_entry = DateEntry(edit_window, width=30, background='darkblue', 
                                 foreground='white', borderwidth=2, date_pattern='y-mm-dd')
    event_date_entry.pack(pady=5)
    event_date_entry.set_date(event_date)

    description_label = tk.Label(edit_window, text="Description:")
    description_label.pack(pady=10)
    description_entry = tk.Text(edit_window, height=5, width=30)
    description_entry.pack(pady=5)
    description_entry.insert(tk.END, event_description)

    save_button = tk.Button(edit_window, text="Save Changes", command=lambda: save_edited_event(selected_event, event_name_entry, event_date_entry, description_entry, edit_window))
    save_button.pack(pady=10)

def save_edited_event(selected_event, name_entry, date_entry, description_entry, edit_window):
    new_event_name = name_entry.get()
    new_event_date = date_entry.get_date()
    new_event_description = description_entry.get("1.0", tk.END).strip()

    if new_event_name and new_event_date:
        new_event_details = f"{new_event_name} - {new_event_date} - {new_event_description}"
        update_event_in_file(selected_event, new_event_details)
        messagebox.showinfo("Success", "Event updated successfully!")
        edit_window.destroy()
        display_events()

def update_event_in_file(old_event, new_event):
    events = load_events()
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
root.geometry("600x400")
root.config(bg="#d3d3d3") 

top_frame = tk.Frame(root, bg="#0000FF", height=50) 
top_frame.place(relx=0.0, rely=0.0, relwidth=1, relheight=0.1)


welcome_label = tk.Label(top_frame, text="Welcome, [User's Name]", bg="#0000FF", fg="white", font=("Arial", 16))
welcome_label.pack(side="left", padx=10)

logout_button = tk.Button(top_frame, text="Logout", command=logout, bg="#0000FF", fg="white")
logout_button.pack(side="right", padx=10)


sidebar_frame = tk.Frame(root, bg="#0000FF", width=150)
sidebar_frame.place(relx=0.0, rely=0.1, relheight=0.9, relwidth=0.25)

img = Image.open("user.png")


resized_img = img.resize((50, 50), Image.LANCZOS)  


photo_img = ImageTk.PhotoImage(resized_img)

root.profile_icon = photo_img


profile_icon_label = tk.Label(sidebar_frame, image=root.profile_icon, bg="#0000FF")
profile_icon_label.pack(pady=20) 

create_events_button = tk.Button(sidebar_frame, text="Create Events", command=show_create_event_form, bg="#0000FF", fg="white") 
create_events_button.pack(fill="x", pady=10)


guest_list_button = tk.Button(sidebar_frame, text="Guest List", command=show_create_guest_form, bg="#0000FF", fg="white")  
guest_list_button.pack(fill="x", pady=10)

View_guest_button = tk.Button(sidebar_frame, text="View Guests", command= show_view_guest_list_form, bg="#0000FF", fg="white")
View_guest_button.pack(fill="x", pady=10)


main_content = tk.Frame(root, bg="white")
main_content.place(relx=0.25, rely=0.1, relwidth=0.85, relheight=0.9)



display_events()

root.mainloop()

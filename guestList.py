import smtplib
import email
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import messagebox, ttk
import uuid
import re

# Email configuration
EMAIL_USERNAME = "zimkhitha.nongomaza@capaciti.org.za"
EMAIL_PASSWORD = "Losiwe@1"
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587

# Function to generate unique access link
def generate_access_link(guest_name):
    return f"http://localhost:8080/guest/{uuid.uuid4()}"

# Function to send email invitation
def send_invitation(guest_name, guest_email):
    access_link = generate_access_link(guest_name)
    msg = MIMEText(f"Dear {guest_name},\n\nYou're invited to our event! Please click this link to RSVP: {access_link}\n\nBest regards, [Your Name]")
    msg['Subject'] = "Event Invitation"
    msg['From'] = EMAIL_USERNAME
    msg['To'] = guest_email

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
    server.sendmail(EMAIL_USERNAME, guest_email, msg.as_string())
    server.quit()

# Function to validate email
def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)

# Function to validate cellphone number
def validate_cellphone(cellphone):
    pattern = r"^\d{10}$"
    return re.match(pattern, cellphone)

# Function to validate name
def validate_name(name):
    pattern = r"^[a-zA-Z\s]+$"
    return re.match(pattern, name)

# Function to add guest to list and send invitation
def add_guest():
    guest_name = name_entry.get()
    guest_email = email_entry.get()
    guest_cellphone = cellphone_entry.get()
   

    if not validate_name(guest_name):
        messagebox.showerror("Error", "Invalid name.")
        return

    if not validate_email(guest_email):
        messagebox.showerror("Error", "Invalid email.")
        return

    if not validate_cellphone(guest_cellphone):
        messagebox.showerror("Error", "Invalid cellphone number.")
        return

    if guest_name and guest_email and guest_cellphone:
        # Add guest to text file
        with open("guest.txt", "a") as file:
            file.write(f"{guest_name},{guest_email},{guest_cellphone}\n")

        # Send email invitation
        send_invitation(guest_name, guest_email)
        messagebox.showinfo("Success", "Guest added and invitation sent!")
        name_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        cellphone_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please fill in all fields.")
        
        
    

# Function to view guest list
def view_guests():
    tree.delete(*tree.get_children())
    try:
        with open("guest.txt", "r") as file:
            guests = file.readlines()
            for guest in guests:
                name, email, cellphone = guest.strip().split(",")
                tree.insert("", tk.END, values=(name, email, cellphone))
    except FileNotFoundError:
        messagebox.showerror("Error", "No guests added yet.")

# Function to delete selected guest
def delete_guest():
    selected = tree.focus()
    if selected:
        tree.delete(selected)
        with open("guest.txt", "r") as file:
            guests = file.readlines()
        with open("guest.txt", "w") as file:
            for guest in guests:
                name, email, cellphone = guest.strip().split(",")
                if name != tree.item(selected, "values")[0]:
                    file.write(guest)
        messagebox.showinfo("Success", "Guest deleted.")
    else:
        messagebox.showerror("Error", "Please select a guest.")

# Function to update selected guest
def update_guest():
    selected = tree.focus()
    if selected:
        name = tree.item(selected, "values")[0]
        email = tree.item(selected, "values")[1]
        cellphone = tree.item(selected, "values")[2]
        update_window = tk.Toplevel()
        update_window.title("Update Guest")

        name_label = tk.Label(update_window, text="Name:")
        name_label.pack()
        name_entry = tk.Entry(update_window)
        name_entry.insert(0, name)
        name_entry.pack()

        email_label = tk.Label(update_window, text="Email:")
        email_label.pack()
        email_entry = tk.Entry(update_window)
        email_entry.insert(0, email)
        email_entry.pack()

        cellphone_label = tk.Label(update_window, text="Cellphone:")
        cellphone_label.pack()
        cellphone_entry = tk.Entry(update_window)
        cellphone_entry.insert(0, cellphone)
        cellphone_entry.pack()

        def save_update():
            new_name = name_entry.get()
            new_email = email_entry.get()
            new_cellphone = cellphone_entry.get()

            if not validate_name(new_name):
                messagebox.showerror("Error", "Invalid name.")
                return

            if not validate_email(new_email):
                messagebox.showerror("Error", "Invalid email.")
                return

            if not validate_cellphone(new_cellphone):
                messagebox.showerror("Error", "Invalid cellphone number.")
                return

            with open("guest.txt", "r") as file:
                guests = file.readlines()
            with open("guest.txt", "w") as file:
                for guest in guests:
                    guest_name, guest_email, guest_cellphone = guest.strip().split(",")
                    if guest_name == name:
                        file.write(f"{new_name},{new_email},{new_cellphone}\n")
                    else:
                        file.write(guest)
            tree.item(selected, values=(new_name, new_email, new_cellphone))
            update_window.destroy()
            messagebox.showinfo("Success", "Guest updated.")

        save_button = tk.Button(update_window, text="Save", command=save_update)
        save_button.pack()
    else:
        messagebox.showerror("Error", "Please select a guest.")

  # Clear input fields
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    cellphone_entry.delete(0, tk.END)

# Create GUI
root = tk.Tk()
root.title("Guest List System")

name_label = tk.Label(root, text="Name:")
name_label.pack()
name_entry = tk.Entry(root)
name_entry.pack()

email_label = tk.Label(root, text="Email:")
email_label.pack()
email_entry = tk.Entry(root)
email_entry.pack()

cellphone_label = tk.Label(root, text="Cellphone:")
cellphone_label.pack()
cellphone_entry = tk.Entry(root)
cellphone_entry.pack()

add_button = tk.Button(root, text="Add Guest", command=add_guest)
add_button.pack()

view_button = tk.Button(root, text="View Guests", command=view_guests)
view_button.pack()

delete_button = tk.Button(root, text="Delete Guest", command=delete_guest)
delete_button.pack()

update_button = tk.Button(root, text="Update Guest", command=update_guest)
update_button.pack()

tree = ttk.Treeview(root)
tree['columns'] = ('Name', 'Email', 'Cellphone')
tree.column("#0", width=0, )
tree.column("Name", anchor=tk.W, width=100)
tree.column("Email", anchor=tk.W, width=150)
tree.column("Cellphone", anchor=tk.W, width=100)
tree.heading("#0", text='', anchor=tk.W)
tree.heading("Name", text='Name', anchor=tk.W)
tree.heading("Email", text='Email', anchor=tk.W)
tree.heading("Cellphone", text='Cellphone', anchor=tk.W)
tree.pack()

#adding a scroller

root.mainloop()


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import tkinter as tk
from tkinter import Listbox, Scrollbar, messagebox, simpledialog, ttk
from datetime import datetime
import re
import secrets
import string

class Event:
    def __init__(self, name, date, location, description, password=None):
        self.name = name
        self.date = date
        self.location = location
        self.description = description
        self.password = password or self.generate_password()

    def generate_password(self, length=12):
        alphabet = string.ascii_letters
        digits = string.digits
        symbols = string.punctuation
        all_characters = alphabet + digits + symbols

        password = [
            secrets.choice(alphabet),
            secrets.choice(digits),
            secrets.choice(symbols)
        ]
        password += [secrets.choice(all_characters) for _ in range(length - 3)]
        secrets.SystemRandom().shuffle(password)

        return ''.join(password)

    @staticmethod
    def save_event(event):
        with open("Event.txt", "a") as file:
            file.write(f'{event.name}, {event.date}, {event.location}, {event.description}, {event.password}\n')

    @staticmethod
    def load_events():
        events = []
        try:
            with open("Event.txt", "r") as file:
                for line in file:
                    name, date, location, description, password = line.strip().split(", ")
                    events.append(Event(name, date, location, description, password))
        except FileNotFoundError:
            pass
        return events

    @staticmethod
    def delete_event(name):
        events = Event.load_events()
        events = [event for event in events if event.name != name]

        with open("Event.txt", "w") as file:
            for event in events:
                file.write(f'{event.name}, {event.date}, {event.location}, {event.description}, {event.password}\n')


class EventApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Manager")
        self.root.geometry("600x400")
        self.root.config(bg="#f5f5f5")

        self.form_frame = tk.Frame(self.root, bg="#ffffff", padx=20, pady=20)
        self.form_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Create input fields
        self.label_title = tk.Label(self.form_frame, text="Event Details", font=("Arial", 18), bg="#ffffff")
        self.label_title.pack(pady=(0, 20))

        self.label_event_name = tk.Label(self.form_frame, text="Event Name:", bg="#ffffff")
        self.label_event_name.pack(anchor='w')
        self.entry_event_name = tk.Entry(self.form_frame, font=("Arial", 12), width=30)
        self.entry_event_name.pack(pady=(0, 10))

        self.label_event_date = tk.Label(self.form_frame, text="Event Date (YYYY/MM/DD):", bg="#ffffff")
        self.label_event_date.pack(anchor='w')
        self.date_entry = tk.Entry(self.form_frame,font=("Arial", 12), width=30)
        self.date_entry.pack(pady=(0,20)

        # Create a Date Picker using ttk.Combobox
        
        self.label_event_location = tk.Label(self.form_frame, text="Event Location:", bg="#ffffff")
        self.label_event_location.pack(anchor='w')
        self.entry_event_location = tk.Entry(self.form_frame, font=("Arial", 12), width=30)
        self.entry_event_location.pack(pady=(0, 10))

        self.label_event_description = tk.Label(self.form_frame, text="Event Description:", bg="#ffffff")
        self.label_event_description.pack(anchor='w')
        self.entry_event_description = tk.Entry(self.form_frame, font=("Arial", 12), width=30)
        self.entry_event_description.pack(pady=(0, 20))

        # Save button below input fields
        self.save_button = tk.Button(self.form_frame, text="Save Event", command=self.save_event, bg="#4CAF50", fg="white", font=("Arial", 12), padx=10, pady=5)
        self.save_button.pack(pady=(10, 20))

        # Create Listbox with a scrollbar for events
        self.listbox_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.listbox_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.event_listbox = Listbox(self.listbox_frame, font=("Arial", 12), bg="#ffffff", selectbackground="#B2EBF2", height=15)
        self.event_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.scrollbar = Scrollbar(self.listbox_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.event_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.event_listbox.yview)

        # Create a button frame at the bottom of the listbox
        self.button_frame = tk.Frame(self.listbox_frame, bg="#f5f5f5")
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Buttons for Edit and Delete at the bottom
        self.edit_button = tk.Button(self.button_frame, text="Edit Event", command=self.edit_event, bg="#FFC107", fg="black", font=("Arial", 12), padx=10, pady=5)
        self.edit_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete Event", command=self.delete_event, bg="#F44336", fg="white", font=("Arial", 12), padx=10, pady=5)
        self.delete_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Load existing events
        self.load_events()

    def validate_fields(self, name, date, location, description):
        # Check if any field is empty
        if not name or not date or not location or not description:
            return False, "All fields must be filled."

        # Check if date is in the correct format
        try:
            datetime.strptime(date, '%Y/%m/%d')  # Validates the date format
        except ValueError:
            return False, "Date must be in the format YYYY/MM/DD."

        return True, ""

    def save_event(self):
        name = self.entry_event_name.get()
        date = self.date_combobox.get()  # Get date from Combobox
        location = self.entry_event_location.get()
        description = self.entry_event_description.get()

        # Validate fields
        is_valid, message = self.validate_fields(name, date, location, description)
        if not is_valid:
            messagebox.showwarning("Validation Error", message)
            return

        # Save event if valid
        event = Event(name, date, location, description)
        Event.save_event(event)
        self.clear_entries()
        self.load_events()

    def load_events(self):
        self.event_listbox.delete(0, tk.END)
        events = Event.load_events()
        for event in events:
            self.event_listbox.insert(tk.END, event.name)

    def edit_event(self):
        selected_event_index = self.event_listbox.curselection()
        if selected_event_index:
            selected_event_name = self.event_listbox.get(selected_event_index)
            events = Event.load_events()
            selected_event = next((event for event in events if event.name == selected_event_name), None)

            new_name = simpledialog.askstring("Edit Event", "New Event Name:", initialvalue=selected_event.name)
            new_date = simpledialog.askstring("Edit Event", "New Date (YYYY/MM/DD):", initialvalue=selected_event.date)
            new_location = simpledialog.askstring("Edit Event", "New Location:", initialvalue=selected_event.location)
            new_description = simpledialog.askstring("Edit Event", "New Description:", initialvalue=selected_event.description)

            if new_name and new_date and new_location and new_description:
                # Validate edited fields
                is_valid, message = self.validate_fields(new_name, new_date, new_location, new_description)
                if not is_valid:
                    messagebox.showwarning("Validation Error", message)
                    return

                Event.delete_event(selected_event.name)
                edited_event = Event(new_name, new_date, new_location, new_description)
                Event.save_event(edited_event)
                self.load_events()
            else:
                messagebox.showwarning("Input Error", "Please fill in all fields.")
        else:
            messagebox.showwarning("Selection Error", "Please select an event to edit.")

    def delete_event(self):
        selected_event_index = self.event_listbox.curselection()
        if selected_event_index:
          
            selected_event_name = self.event_listbox.get(selected_event_index)
            Event.delete_event(selected_event_name)
            self.load_events()
        else:
            messagebox.showwarning("Selection Error", "Please select an event to delete.")

    def clear_entries(self):
        self.entry_event_name.delete(0, tk.END)
        self.entry_event_date.delete(0, tk.END)
        self.entry_event_location.delete(0, tk.END)
        self.entry_event_description.delete(0, tk.END)


def send_email(self, event, guest_email):
    sender_email = "ntombekhaya.mkaba@capaciti.org.za" 
    sender_password = "Ntosh98*#"  
    subject = "Invitation to Event: " + event.name

    # Create the email body
    body = f"""
    Dear Guest,

    You are invited to the event "{event.name}".
    
    Event Details:
    - Date: {event.date}
    - Location: {event.location}
    - Description: {event.description}
    
    Your secret password to access the event is: {event.password}

    We look forward to seeing you there!

    Best regards,
    Event Manager Team
    """
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = guest_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    # Set up the server connection and send the email
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)  # For Gmail
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, guest_email, msg.as_string())
        server.quit()

        messagebox.showinfo("Success", f"Email sent to {guest_email}!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email. Error: {str(e)}")

def save_event(self):
    name = self.entry_event_name.get()
    date = self.date_combobox.get()  # Get date from Combobox
    location = self.entry_event_location.get()
    description = self.entry_event_description.get()

    if self.validate_inputs(name, date, location, description):
        event = Event(name, date, location, description)
        Event.save_event(event)
        
        # Prompt for guest email address to send the invitation
        guest_email = simpledialog.askstring("Guest Email", "Enter the guest's email address:")
        if guest_email:
            self.send_email(event, guest_email)
        
        self.clear_entries()
        self.load_events()
    
# Main application
root = tk.Tk()
app = EventApp(root)
root.mainloop()    
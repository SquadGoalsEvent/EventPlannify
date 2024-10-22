import tkinter as tk
from tkinter import ttk, messagebox
import smtplib
from email.mime.text import MIMEText
import uuid
import re


# Email configuration
EMAIL_USERNAME = "zimkhitha.nongomaza@capaciti.org.za"
EMAIL_PASSWORD = "Losiwe@1"
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587

# Function to generate unique password
def generate_password():
  return str(uuid.uuid4())

# Function to generate unique access link 
def generate_access_link(guest_name):
  return f"http://localhost:8080/guest/{uuid.uuid4()}"

# Function to send email invitation
def send_invitation(guest_name, guest_email, password):
  access_link = generate_access_link(guest_name)
  msg = MIMEText(f"Dear {guest_name},\n\nYou're invited to our event! Your password is:\n {password} \n\n Click on the link to RSVP {access_link} \n\nBest regards,\n Zimi Nongomaza")
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
      password = generate_password()
      # Add guest to text file
      with open("guestlist.txt", "a") as file:
          file.write(f"{guest_name},{guest_email},{guest_cellphone},{password}\n")
      # Send email invitation
      send_invitation(guest_name, guest_email, password)
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
      with open("guestlist.txt", "r") as file:
          guests = file.readlines()
      for guest in guests:
          name, email, cellphone, _ = guest.strip().split(",")
          tree.insert("", tk.END, values=(name, email, cellphone))
  except FileNotFoundError:
      messagebox.showerror("Error", "No guests added yet.")

def view_rsvp():
  tree.delete(*tree.get_children())
  try:
      with open("rsvp.txt", "r") as file:
          rsvps = file.readlines()
      for rsvp in rsvps:
          name, email = rsvp.strip().split(",")
          tree.insert("", tk.END, values=(name, email))
  except FileNotFoundError:
      messagebox.showerror("Error", "No guests added yet.")

# Function to delete selected guest
def delete_guest():
  selected = tree.focus()
  if selected:
      tree.delete(selected)
      with open("guestlist.txt", "r") as file:
          guests = file.readlines()
      with open("guestlist.txt", "w") as file:
          for guest in guests:
              name, email, cellphone, _ = guest.strip().split(",")
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
      update_window.geometry("300x200")
      main_frame = tk.Frame(update_window, bg="#2C3E50")
      main_frame.pack(fill="both", expand=True)

      # Create labels and entries
      name_label = tk.Label(main_frame, text="Name:", bg="#2C3E50", fg="#ECF0F1")
      name_label.grid(row=0, column=0, padx=5, pady=5)
      name_entry = tk.Entry(main_frame, bg="#95A5A6", fg="#ECF0F1")
      name_entry.grid(row=0, column=1, padx=5, pady=5)

      email_label = tk.Label(main_frame, text="Email:", bg="#2C3E50", fg="#ECF0F1")
      email_label.grid(row=1, column=0, padx=5, pady=5)
      email_entry = tk.Entry(main_frame, bg="#95A5A6", fg="#ECF0F1")
      email_entry.grid(row=1, column=1, padx=5, pady=5)

      cellphone_label = tk.Label(main_frame, text="Cellphone:", bg="#2C3E50", fg="#ECF0F1")
      cellphone_label.grid(row=2, column=0, padx=5, pady=5)
      cellphone_entry = tk.Entry(main_frame, bg="#95A5A6", fg="#ECF0F1")
      cellphone_entry.grid(row=2, column=1, padx=5, pady=5)

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
          with open("guestlist.txt", "r") as file:
              guests = file.readlines()
          with open("guestlist.txt", "w") as file:
              for guest in guests:
                  guest_name, guest_email, guest_cellphone, password = guest.strip().split(",")
                  if guest_name == name:
                      file.write(f"{new_name},{new_email},{new_cellphone},{password}\n")
                  else:
                      file.write(guest)
          tree.item(selected, values=(new_name, new_email, new_cellphone))
          update_window.destroy()
          messagebox.showinfo("Success", "Guest updated.")

      save_button = tk.Button(main_frame, text="Save", command=save_update, bg="#3498DB", fg="#ECF0F1")
      save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

  else:
      messagebox.showerror("Error", "Please select a guest.")

# Function to RSVP
def rsvp():
  rsvp_window = tk.Toplevel()
  rsvp_window.title("RSVP")
  rsvp_window.geometry("300x200")

  main_frame = tk.Frame(rsvp_window, bg="#2C3E50")
  main_frame.pack(fill="both", expand=True)

  # Create labels and entries
  name_label = tk.Label(main_frame, text="Name:", bg="#2C3E50", fg="#ECF0F1")
  name_label.grid(row=0, column=0, padx=5, pady=5)
  name_entry = tk.Entry(main_frame, bg="#95A5A6", fg="#ECF0F1")
  name_entry.grid(row=0, column=1, padx=5, pady=5)

  email_label = tk.Label(main_frame, text="Email:", bg="#2C3E50", fg="#ECF0F1")
  email_label.grid(row=1, column=0, padx=5, pady=5)
  email_entry = tk.Entry(main_frame, bg="#95A5A6", fg="#ECF0F1")
  email_entry.grid(row=1, column=1, padx=5, pady=5)

  password_label = tk.Label(main_frame, text="Password:", bg="#2C3E50", fg="#ECF0F1")
  password_label.grid(row=2, column=0, padx=5, pady=5)
  password_entry = tk.Entry(main_frame, show="*", bg="#95A5A6", fg="#ECF0F1")
  password_entry.grid(row=2, column=1, padx=5, pady=5)

  def submit_rsvp():
      name = name_entry.get().strip()
      email = email_entry.get().strip()
      password = password_entry.get().strip()

      if not name or not email or not password:
          messagebox.showerror("Error", "Please fill in all fields.")
          return
      try:
          with open("guestlist.txt", "r") as file:
              guests = file.readlines()
          for guest in guests:
              guest_info = guest.strip().split(",")
              if len(guest_info) < 4:
                  messagebox.showerror("Error", "Invalid guest information.")
                  continue
              guest_name, guest_email, _, guest_password = guest_info
              if guest_name == name and guest_email == email and guest_password == password:
                  # RSVP successful
                  with open("rsvp.txt", "a") as rsvp_file:
                      rsvp_file.write(f"{name},{email}\n")
                  messagebox.showinfo("Success", "RSVP successful!")
                  rsvp_window.destroy()
                  break
          else:
              messagebox.showerror("Error", "Invalid credentials.")
      except FileNotFoundError:
          messagebox.showerror("Error", "Guest list file not found.")
      except Exception as e:
          messagebox.showerror("Error", str(e))

  submit_button = tk.Button(main_frame, text="Submit RSVP", command=submit_rsvp, bg="#3498DB", fg="#ECF0F1")
  submit_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Create GUI
root = tk.Tk()
root.title("Guest List System")

# Set theme colors
primary_color = "#2C3E50"
secondary_color = "#95A5A6"
accent_color = "#3498DB"
text_color = "#ECF0F1"

# Create main frames
input_frame = tk.Frame(root, bg=primary_color) 
input_frame.pack(fill="both", expand=True)

button_frame = tk.Frame(root, bg=primary_color)
button_frame.pack(fill="x")

tree_frame = tk.Frame(root, bg=primary_color) 
tree_frame.pack(fill="both", expand=True)

# Create input frame widgets
name_label = tk.Label(input_frame, text="Name:", bg=primary_color, fg=text_color) 
name_label.grid(row=0, column=0, padx=5, pady=5) 
name_entry = tk.Entry(input_frame, bg=secondary_color, fg=text_color) 
name_entry.grid(row=0, column=1, padx=5, pady=5)

email_label = tk.Label(input_frame, text="Email:", bg=primary_color, fg=text_color) 
email_label.grid(row=1, column=0, padx=5, pady=5) 
email_entry = tk.Entry(input_frame, bg=secondary_color, fg=text_color)
email_entry.grid(row=1, column=1, padx=5, pady=5)

cellphone_label = tk.Label(input_frame, text="Cellphone:", bg=primary_color, fg=text_color) 
cellphone_label.grid(row=2, column=0, padx=5, pady=5) 
cellphone_entry = tk.Entry(input_frame, bg=secondary_color, fg=text_color) 
cellphone_entry.grid(row=2, column=1, padx=5, pady=5)

# Create button frame widgets
add_button = tk.Button(button_frame, text="Add Guest", command=add_guest, bg=accent_color, fg=text_color) 
add_button.pack(side="left", fill="x", expand=True)

view_button = tk.Button(button_frame, text="View Guests", command=view_guests, bg=accent_color, fg=text_color) 
view_button.pack(side="left", fill="x", expand=True)

delete_button = tk.Button(button_frame, text="Delete Guest", command=delete_guest, bg=accent_color, fg=text_color) 
delete_button.pack(side="left", fill="x", expand=True)

update_button = tk.Button(button_frame, text="Update Guest", command=update_guest, bg=accent_color, fg=text_color) 
update_button.pack(side="left", fill="x", expand=True)

rsvp_button = tk.Button(button_frame, text="RSVP", command=rsvp, bg=accent_color, fg=text_color)
rsvp_button.pack(side="left", fill="x", expand=True)

view_button = tk.Button(button_frame, text="View RSVPS", command=view_rsvp, bg=accent_color, fg=text_color) 
view_button.pack(side="left", fill="x", expand=True)

# Create tree frame widget
tree = ttk.Treeview(tree_frame)
tree['columns'] = ('Name', 'Email', 'Cellphone') 
tree.column("#0", width=0)
tree.column("Name", anchor=tk.W, width=100) 
tree.column("Email", anchor=tk.W, width=150) 
tree.column("Cellphone", anchor=tk.W, width=100) 
tree.heading("#0", text='', anchor=tk.W) 
tree.heading("Name", text='Name', anchor=tk.W) 
tree.heading("Email", text='Email', anchor=tk.W) 
tree.heading("Cellphone", text='Cellphone', anchor=tk.W) 
tree.pack(fill="both", expand=True)

root.resizable(True, True)
root.mainloop()


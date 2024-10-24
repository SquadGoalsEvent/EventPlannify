import tkinter as tk
from tkinter import Image, ttk, messagebox
import smtplib
from email.mime.text import MIMEText
import uuid
import re
import tkinter.font as tkFont
from PIL import Image, ImageTk 



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
    msg = MIMEText(f"Dear {guest_name},\n\nYou're invited to our event! Your password is:\n {password} \n\n Click on the link to RSVP {access_link} \n\nBest regards,\n Your Name")
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
    if not re.match(pattern, email):
        messagebox.showerror("Invalid Email", "Please enter a valid email address")
        return None
    local_part, domain_part = email.split('@')
    local_part = local_part.replace('.', '')
    domain_part = domain_part.lower()
    return f"{local_part}@{domain_part}"

# Function to validate cellphone number
def validate_cellphone(cellphone):
    pattern = r"^\d{10}$"
    return re.match(pattern, cellphone)

# Function to validate name
def validate_name(name):
    pattern = r"^[a-zA-Z\s]+$"
    return re.match(pattern, name)

# Function to add guest to list and send invitation 

def add_guest_window():
    # Create a new window for adding a guest
    add_guest_win = tk.Toplevel()
    add_guest_win.title("Add Guest")
    add_guest_win.geometry("400x300")
    
    main_frame = tk.Frame(add_guest_win)
    main_frame.pack(pady=20, padx=20, fill="x")

    # Input fields for guest information
    name_label = tk.Label(main_frame, text="Name:", font=('Microsoft YaHei UI Light', 12))
    name_label.pack(pady=5)
    name_entry = tk.Entry(main_frame, width=30)
    name_entry.pack(pady=5)

    email_label = tk.Label(main_frame, text="Email:", font=('Microsoft YaHei UI Light', 12))
    email_label.pack(pady=5)
    email_entry = tk.Entry(main_frame, width=30)
    email_entry.pack(pady=5)

    cellphone_label = tk.Label(main_frame, text="Cellphone:", font=('Microsoft YaHei UI Light', 12))
    cellphone_label.pack(pady=5)
    cellphone_entry = tk.Entry(main_frame, width=30)
    cellphone_entry.pack(pady=5)

    def add_guest():
        name = name_entry.get()
        email = email_entry.get()
        cellphone = cellphone_entry.get()
        
        if not validate_name(name):
            messagebox.showerror("Error", "Invalid name.")
            return
        if not validate_email(email):
            messagebox.showerror("Error", "Invalid email.")
            return
        if not validate_cellphone(cellphone):
            messagebox.showerror("Error", "Invalid cellphone number.")
            return
        
        if name and email and cellphone:
            password = generate_password()
            # Add guest to text file
            with open("guestlist.txt", "a") as file:
                file.write(f"{name},{email},{cellphone},{password}\n")
            # Send email invitation
            send_invitation(name, email, password)
            messagebox.showinfo("Success", "Guest added and invitation sent!")
            name_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            cellphone_entry.delete(0, tk.END)
            add_guest_win.destroy()  # Close the window after adding the guest
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    # Add button to save guest
    add_button = tk.Button(main_frame, text="Add Guest", command=add_guest, bg="#800080", fg='white', font=('Microsoft YaHei UI Light', 12))
    add_button.pack(pady=20)

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
        messagebox.showerror("Error", "No RSVPs found.")

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
        update_window.geometry("400x300")
        main_frame = tk.Frame(update_window,)
        main_frame.pack(fill="both", expand=True)

        # Create labels and entries
        name_label = tk.Label(main_frame, text="Name:", font=('Microsoft YaHei UI Light', 12))
        name_label.pack(pady=5)
        name_entry = tk.Entry(main_frame, width=30)
        name_entry.pack(pady=5)

        email_label = tk.Label(main_frame, text="Email:", font=('Microsoft YaHei UI Light', 12))
        email_label.pack(pady=5)
        email_entry = tk.Entry(main_frame, width=30)
        email_entry.pack(pady=5)

        cellphone_label = tk.Label(main_frame, text="Cellphone:", font=('Microsoft YaHei UI Light', 12))
        cellphone_label.pack(pady=5)
        cellphone_entry = tk.Entry(main_frame, width=30)
        cellphone_entry.pack(pady=5)

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

        add_button = tk.Button(main_frame, text="UPDATE GUEST", command=save_update, bg="#800080", fg='white', font=('Microsoft YaHei UI Light', 12))
        add_button.pack(pady=20)
    else:
        messagebox.showerror("Error", "Please select a guest.")

# Function to RSVP
def rsvp():
    rsvp_window = tk.Toplevel()
    rsvp_window.title("RSVP")
    rsvp_window.geometry("400x300")

    main_frame = tk.Frame(rsvp_window)
    main_frame.pack(fill="both", expand=True)

    # Create labels and entries
    name_label = tk.Label(main_frame, text="Name:",font=('Microsoft YaHei UI Light', 12))
    name_label.pack(pady=5)
    name_entry = tk.Entry(main_frame, width=30)
    name_entry.pack(pady=5)
 
    email_label = tk.Label(main_frame, text="Email:", font=('Microsoft YaHei UI Light', 12))
    email_label.pack(pady=5)
    email_entry = tk.Entry(main_frame, width=30)
    email_entry.pack(pady=5)

    password_label = tk.Label(main_frame, text="Password:", font=('Microsoft YaHei UI Light', 12))
    password_label.pack(pady=5)
    password_entry = tk.Entry(main_frame, width=30)
    password_entry.pack(pady=5)


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

 

    add_button = tk.Button(main_frame, text="Submit RSVP", command=submit_rsvp, bg="#800080", fg='white', font=('Microsoft YaHei UI Light', 12))
    add_button.pack(pady=20)

def logout():
        response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if response:
          root.quit()



# Create GUI
root = tk.Tk()
root.title("Guest List System")
root.geometry("1500x800")




top_frame = tk.Frame(root, bg="#800080", height=50)
top_frame.place(relx=0.0, rely=0.0, relwidth=1, relheight=0.1)

# Create the logout button
logout_button = tk.Button(top_frame, text="Logout", command=logout, bg="#800080", fg="white")
logout_button.pack(side="right", padx=10)

# Set theme colors
primary_color = "#2C3E50"  # Dark purple
secondary_color = "#8E44AD"  # Lighter purple
accent_color = "#3498DB"  # Blue for buttons
text_color = "#ECF0F1"  # Light text color

# Create sidebar frame for buttons
sidebar_frame = tk.Frame(root, bg="#800080",width=150)
sidebar_frame.place(relx=0.0, rely=0.1, relheight=0.9, relwidth=0.25)


# Create the sidebar frame
sidebar_frame = tk.Frame(root, bg="#800080", width=150)
sidebar_frame.place(relx=0.0, rely=0.1, relheight=0.9, relwidth=0.25)

# Create the welcome label under the icon
welcome_label = tk.Label(sidebar_frame, text="Welcome,", bg="#800080", fg="white", font=("Microsoft YaHei UI Light", 20))
welcome_label.pack(pady=15) 

# Load profile icon
img = Image.open("user.png ")
resized_img = img.resize((50, 50), Image.LANCZOS)
photo_img = ImageTk.PhotoImage(resized_img)
root.profile_icon = photo_img
profile_icon_label = tk.Label(sidebar_frame, image=root.profile_icon, bg="#800080")
profile_icon_label.pack(pady=20)

# Centering the buttons in the sidebar
button_frame = tk.Frame(sidebar_frame, bg="#800080")
button_frame.pack(fill="x", pady=(1, 5))

# Create main content frame for labels and entry inputs
main_frame = tk.Frame(root, bg=primary_color)
main_frame.place(relx=0.25, rely=0.1, relwidth=0.75, relheight=0.9)  # Adjusted width


# Function to create a button with an icon and text
def create_button_with_icon(frame, text, command):
    button = tk.Button(frame, text=text, command=command, bg="#800080", fg="white", font=("Microsoft YaHei UI Light", 20),  compound="left")
    button.pack(fill="x", pady=(2, 6))  


# Create buttons with icons
create_button_with_icon(sidebar_frame, "ADD GUEST", add_guest_window)
create_button_with_icon(sidebar_frame, "VIEW GUEST", view_guests)
create_button_with_icon(sidebar_frame, "DELETE GUEST", delete_guest)
create_button_with_icon(sidebar_frame, "UPDATE GUEST", update_guest)
create_button_with_icon(sidebar_frame, "MAKE AN RSVP", rsvp)
create_button_with_icon(sidebar_frame, "VIEW RSVP", view_rsvp)




# Create sidebar button widgets with padding


# Create tree frame widget for displaying guest list
tree_frame = tk.Frame(main_frame, bg=primary_color) 
tree_frame.grid(row=3, column=0, columnspan=2, sticky="nsew")  # Place treeview below inputs
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 14, "bold"), foreground="#800080")  # Change the font size, family, and color
style.configure("Treeview", font=("Arial", 11))  # Set the font for the rows


# Configure grid weights for responsive design
main_frame.grid_rowconfigure(3, weight=1)  # Allow treeview to expand
main_frame.grid_columnconfigure(0, weight=1)  # Allow left column to expand
main_frame.grid_columnconfigure(1, weight=1)  # Allow right column to expand



# Create tree view widget
tree = ttk.Treeview(tree_frame, columns=('Name', 'Email', 'Cellphone'), show='headings')


tree.heading("Name", text='Name')
tree.heading("Email", text='Email')
tree.heading("Cellphone", text='Cellphone')

tree.column("Name", anchor="center", width=200)  # You can adjust the width as needed
tree.column("Email", anchor="center", width=200)
tree.column("Cellphone", anchor="center", width=200)

# Configure scrollbar for the treeview
scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)

# Pack the scrollbar and treeview
scrollbar.pack(side='right', fill='y')  # Scrollbar on the right side
tree.pack(side='left', fill='both', expand=True)  # Treeview fills remaining space

# Make sure the sidebar and main frame are responsive
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)  # Sidebar
root.grid_columnconfigure(1, weight=3,)  # Main content
# Set the minimum size for the window
root.minsize(400, 300)

root.resizable(True, True)
root.mainloop()




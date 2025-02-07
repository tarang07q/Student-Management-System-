import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox

conn = None
cursor = None

# Connecting to Database
def create_database():
    global conn, cursor
    try:
        conn = mysql.connector.connect(
            host="0.0.0.0",  # Replace with your MySQL server IP
            user="root",     # Replace with your MySQL username
            password="*********",  # Replace with your MySQL password
            database="student_registration_db"  # Replace with your database name
        )
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS STUD_REGISTRATION (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                contact VARCHAR(50),
                email VARCHAR(255),
                roll_no INT,
                branch VARCHAR(50),
                teacher_id INT,
                course_id INT
            )
        ''')
        conn.commit()
    except Error as e:
        messagebox.showerror("Error", f"Database connection failed: {e}")
        conn = None
        cursor = None

# Check database connection
def check_db_connection():
    if conn is None or cursor is None:
        messagebox.showerror("Error", "Database connection not established.")
        return False
    return True

# Register a new student
def register():
    if not check_db_connection():
        return

    name = name_entry.get()
    contact = contact_entry.get()
    email = email_entry.get()
    roll_no = roll_no_entry.get()
    branch = branch_entry.get()
    teacher_id = teacher_id_entry.get()
    course_id = course_id_entry.get()

    if not all([name, contact, email, roll_no, branch, teacher_id, course_id]):
        messagebox.showinfo("Error", "Please fill in all fields.")
        return

    try:
        cursor.execute('''
            INSERT INTO STUD_REGISTRATION (name, contact, email, roll_no, branch, teacher_id, course_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (name, contact, email, int(roll_no), branch, int(teacher_id), int(course_id)))
        conn.commit()
        messagebox.showinfo("Success", "Student registered successfully.")
        clear_fields()
    except Error as e:
        messagebox.showerror("Error", f"Failed to register student: {e}")

# Display all students
def display_data():
    if not check_db_connection():
        return

    try:
        cursor.execute("SELECT * FROM STUD_REGISTRATION")
        data = cursor.fetchall()

        tree.delete(*tree.get_children())
        for row in data:
            tree.insert("", "end", values=row)
    except Error as e:
        messagebox.showerror("Error", f"Failed to display data: {e}")

# Delete a student record
def delete_data():
    if not check_db_connection():
        return

    selected_item = tree.selection()
    if not selected_item:
        messagebox.showinfo("Error", "Please select a student to delete.")
        return

    item_id = tree.item(selected_item)['values'][0]
    if messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
        try:
            cursor.execute("DELETE FROM STUD_REGISTRATION WHERE id = %s", (item_id,))
            conn.commit()
            messagebox.showinfo("Success", "Student deleted successfully.")
            display_data()
        except Error as e:
            messagebox.showerror("Error", f"Failed to delete student: {e}")

# Clear input fields
def clear_fields():
    name_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    roll_no_entry.delete(0, tk.END)
    branch_entry.delete(0, tk.END)
    teacher_id_entry.delete(0, tk.END)
    course_id_entry.delete(0, tk.END)

# GUI Setup
window = tk.Tk()
window.title("Student Management System")

# Input Fields
tk.Label(window, text="Name:").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(window)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(window, text="Contact:").grid(row=1, column=0, padx=5, pady=5)
contact_entry = tk.Entry(window)
contact_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(window, text="Email:").grid(row=2, column=0, padx=5, pady=5)
email_entry = tk.Entry(window)
email_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(window, text="Roll No:").grid(row=3, column=0, padx=5, pady=5)
roll_no_entry = tk.Entry(window)
roll_no_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(window, text="Branch:").grid(row=4, column=0, padx=5, pady=5)
branch_entry = tk.Entry(window)
branch_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Label(window, text="Teacher ID:").grid(row=5, column=0, padx=5, pady=5)
teacher_id_entry = tk.Entry(window)
teacher_id_entry.grid(row=5, column=1, padx=5, pady=5)

tk.Label(window, text="Course ID:").grid(row=6, column=0, padx=5, pady=5)
course_id_entry = tk.Entry(window)
course_id_entry.grid(row=6, column=1, padx=5, pady=5)

# Buttons
tk.Button(window, text="Register", command=register).grid(row=7, column=0, padx=5, pady=5)
tk.Button(window, text="Display Data", command=display_data).grid(row=7, column=1, padx=5, pady=5)
tk.Button(window, text="Delete", command=delete_data).grid(row=7, column=2, padx=5, pady=5)
tk.Button(window, text="Clear", command=clear_fields).grid(row=7, column=3, padx=5, pady=5)

# Treeview for Data Display
tree = ttk.Treeview(window, columns=("ID", "Name", "Contact", "Email", "Roll No", "Branch", "Teacher ID", "Course ID"), show='headings')
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Contact", text="Contact")
tree.heading("Email", text="Email")
tree.heading("Roll No", text="Roll No")
tree.heading("Branch", text="Branch")
tree.heading("Teacher ID", text="Teacher ID")
tree.heading("Course ID", text="Course ID")
tree.grid(row=8, column=0, columnspan=4, padx=5, pady=5)

# Initialize Database and Show Data
create_database()
display_data()

window.mainloop()

# Close database connection on exit
if conn:
    cursor.close()
    conn.close()

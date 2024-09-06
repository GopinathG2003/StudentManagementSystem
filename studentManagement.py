import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database Functions

# Create a SQLite database or connect to one
def connect_db():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    # Create table if not exists
    cur.execute("""
    CREATE TABLE IF NOT EXISTS student (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        grade TEXT
    )
    """)
    conn.commit()
    conn.close()

# Add a new student to the database
def insert_student(name, age, grade):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO student (name, age, grade) VALUES (?, ?, ?)", (name, age, grade))
    conn.commit()
    conn.close()
    view_students()

# Fetch all student records
def view_students():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM student")
    rows = cur.fetchall()
    conn.close()
    return rows

# Delete a student from the database
def delete_student(id):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM student WHERE id=?", (id,))
    conn.commit()
    conn.close()
    view_students()

# Update a student record
def update_student(id, name, age, grade):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("UPDATE student SET name=?, age=?, grade=? WHERE id=?", (name, age, grade, id))
    conn.commit()
    conn.close()
    view_students()

# GUI Functions

def add_student():
    if name_entry.get() == "" or age_entry.get() == "" or grade_entry.get() == "":
        messagebox.showwarning("Input Error", "All fields are required!")
        return
    insert_student(name_entry.get(), age_entry.get(), grade_entry.get())
    clear_inputs()
    view_students_in_listbox()

def remove_student():
    selected_student = student_listbox.curselection()
    if not selected_student:
        messagebox.showwarning("Delete Error", "Select a student to delete")
        return
    student_id = student_listbox.get(selected_student)[0]
    delete_student(student_id)
    view_students_in_listbox()

def modify_student():
    selected_student = student_listbox.curselection()
    if not selected_student:
        messagebox.showwarning("Update Error", "Select a student to update")
        return
    student_id = student_listbox.get(selected_student)[0]
    update_student(student_id, name_entry.get(), age_entry.get(), grade_entry.get())
    clear_inputs()
    view_students_in_listbox()

def clear_inputs():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    grade_entry.delete(0, tk.END)

def view_students_in_listbox():
    student_listbox.delete(0, tk.END)
    for row in view_students():
        student_listbox.insert(tk.END, row)

# Main GUI

# Create main window
root = tk.Tk()
root.title("Student Management System")

# Define Labels
name_label = tk.Label(root, text="Name")
name_label.grid(row=0, column=0, padx=10, pady=10)
age_label = tk.Label(root, text="Age")
age_label.grid(row=1, column=0, padx=10, pady=10)
grade_label = tk.Label(root, text="Grade")
grade_label.grid(row=2, column=0, padx=10, pady=10)

# Define Entry Widgets for input
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=10)
age_entry = tk.Entry(root)
age_entry.grid(row=1, column=1, padx=10, pady=10)
grade_entry = tk.Entry(root)
grade_entry.grid(row=2, column=1, padx=10, pady=10)

# Define Buttons
add_btn = tk.Button(root, text="Add Student", command=add_student)
add_btn.grid(row=3, column=0, padx=10, pady=10)

update_btn = tk.Button(root, text="Update Student", command=modify_student)
update_btn.grid(row=3, column=1, padx=10, pady=10)

delete_btn = tk.Button(root, text="Delete Student", command=remove_student)
delete_btn.grid(row=4, column=0, padx=10, pady=10)

# Define Listbox to show the students
student_listbox = tk.Listbox(root, height=10, width=50)
student_listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Call the function to create or connect to the database
connect_db()

# Populate the Listbox with existing students from the database
view_students_in_listbox()

# Run the application
root.mainloop()

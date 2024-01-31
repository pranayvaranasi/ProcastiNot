from tkinter import *
from tkinter import messagebox
import mysql.connector

# Database connection
db = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    user='pranayvaranasi',
    password='', #password is hidden for privacy reasons
    database='todo'
)

# Function to add a task
def add_task(task_name, description):
    cursor = db.cursor()
    sql = "INSERT INTO tasks (task_name, description, is_completed) VALUES (%s, %s, %s)"
    val = (task_name, description, False)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    messagebox.showinfo('Success', "Task added successfully")
    refresh_tasks()

# Function to delete a task
def delete_task(task_id):
    cursor = db.cursor()
    sql_delete = "DELETE FROM tasks WHERE id = %s"
    val_delete = (task_id,)
    cursor.execute(sql_delete, val_delete)

    # Update task IDs to remain sequential
    sql_update = "ALTER TABLE tasks AUTO_INCREMENT = 1"
    cursor.execute(sql_update)

    db.commit()
    cursor.close()  # Close the cursor after committing the changes
    messagebox.showinfo('Success', "Task deleted successfully")
    refresh_tasks()

# Function to mark a task as completed
def mark_as_completed(task_id):
    cursor = db.cursor()
    sql = "UPDATE tasks SET is_completed = 1 WHERE id = %s"
    val = (task_id,)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    messagebox.showinfo('Success', "Task marked as completed")
    refresh_tasks()

# Function to refresh the displayed tasks
def refresh_tasks():
    for widget in frame_tasks.winfo_children():
        widget.destroy()
    display_tasks()

# Function to display tasks
def display_tasks():
    cursor = db.cursor()
    sql = "SELECT id, task_name, description, is_completed FROM tasks ORDER BY id"
    cursor.execute(sql)
    tasks = cursor.fetchall()
    cursor.close()

    for task in tasks:
        tid, task_name, _description, is_completed = task
        task_background_color = "lightgreen" if is_completed else "lightcoral"
        lbl_task = Label(
            frame_tasks,
            text=f"{tid} - {task_name} [ {'Done' if is_completed else 'Pending'} ]",
            font=("Helvetica", 12),
            pady=5,
            bg=task_background_color
        )
        lbl_task.pack()

        if not is_completed:
            btn_done = Button(
                frame_tasks,
                text="Complete",
                command=lambda t=tid: mark_as_completed(t),
                font=("Helvetica", 10),
                bg="green",
                fg="white",
                padx=8,
                pady=4
            )
            btn_done.pack()

        btn_delete = Button(
            frame_tasks,
            text="Delete",
            command=lambda t=tid: delete_task(t),
            font=("Helvetica", 10),
            bg="red",
            fg="white",
            padx=10,
            pady=4
        )
        btn_delete.pack()

# Main application window
root = Tk()
root.title("Procastinot")
root.geometry("400x400")

# Frame for adding tasks
frame_add = Frame(root, bg="lightblue")
frame_add.pack(pady=10)

lbl_task_name = Label(frame_add, text="Task Name:", font=("Helvetica", 12), bg="lightblue")
lbl_task_name.pack(side=LEFT, padx=5)
ent_task_name = Entry(frame_add, font=("Helvetica", 12))
ent_task_name.pack(side=LEFT, padx=5)

lbl_description = Label(frame_add, text="Description:", font=("Helvetica", 12), bg="lightblue")
lbl_description.pack(side=LEFT, padx=5)
ent_description = Entry(frame_add, font=("Helvetica", 12))
ent_description.pack(side=LEFT, padx=5)

btn_add_task = Button(
    frame_add,
    text="Add Task",
    command=lambda: add_task(ent_task_name.get(), ent_description.get()),
    font=("Helvetica", 12),
    bg="blue",
    fg="white",
    padx=10,
    pady=5
)
btn_add_task.pack(side=LEFT, padx=5)

# Frame for tasks
frame_tasks = Frame(root, bg="lightyellow")
frame_tasks.pack(pady=10)

# Initial refresh of the displayed tasks
refresh_tasks()

root.mainloop()

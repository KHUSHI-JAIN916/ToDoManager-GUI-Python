import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os

FILENAME = "tasks.csv"

def load_tasks():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            return list(csv.reader(file))
    return []

def save_tasks(tasks):
    with open(FILENAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(tasks)

def refresh_list():
    task_table.delete(*task_table.get_children())
    for idx, task in enumerate(load_tasks(), start=1):
        task_table.insert("", "end", values=(idx, task[0], task[1], task[2]))

def add_task():
    title = task_title.get().strip()
    desc = task_desc.get().strip()
    status = "Pending"
    if not title:
        messagebox.showerror("Missing Task", "Please enter a task title.")
        return
    tasks = load_tasks()
    tasks.append([title, desc, status])
    save_tasks(tasks)
    task_title.delete(0, tk.END)
    task_desc.delete(0, tk.END)
    refresh_list()

def mark_done():
    selected = task_table.selection()
    if not selected:
        messagebox.showinfo("No Selection", "Please select a task to mark as done.")
        return
    item = task_table.item(selected[0])
    index = item["values"][0] - 1
    tasks = load_tasks()
    tasks[index][2] = "Done"
    save_tasks(tasks)
    refresh_list()

def delete_task():
    selected = task_table.selection()
    if not selected:
        messagebox.showinfo("No Selection", "Please select a task to delete.")
        return
    index = task_table.item(selected[0])["values"][0] - 1
    tasks = load_tasks()
    tasks.pop(index)
    save_tasks(tasks)
    refresh_list()

# GUI Setup
root = tk.Tk()
root.title("📝 To-Do List Manager")

tk.Label(root, text="Task Title").grid(row=0, column=0)
task_title = tk.Entry(root, width=40)
task_title.grid(row=0, column=1, columnspan=3)

tk.Label(root, text="Description").grid(row=1, column=0)
task_desc = tk.Entry(root, width=40)
task_desc.grid(row=1, column=1, columnspan=3)

tk.Button(root, text="➕ Add Task", command=add_task).grid(row=2, column=1, pady=10)
tk.Button(root, text="✅ Mark as Done", command=mark_done).grid(row=2, column=2)
tk.Button(root, text="❌ Delete Task", command=delete_task).grid(row=2, column=3)

columns = ("S.No", "Title", "Description", "Status")
task_table = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    task_table.heading(col, text=col)
    task_table.column(col, anchor="center")
task_table.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

refresh_list()
root.mainloop()

"""
To-Do List Application - Graphical User Interface Version
This module provides a modern GUI using Tkinter for managing tasks.

Author: Professional Python Developer
Date: 2026-02-17
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from todo_core import TodoManager
from typing import Optional


class TodoGUI:
    """
    Graphical User Interface for the To-Do List application.
    Provides an intuitive interface with buttons, list display, and input fields.
    """
    
    def __init__(self, root):
        """
        Initialize the GUI application.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.manager = TodoManager()
        
        # Configure root window
        self.root.title("To-Do List Application")
        self.root.geometry("900x650")
        self.root.resizable(True, True)
        
        # Set minimum window size
        self.root.minsize(700, 500)
        
        # Configure colors and styles
        self.bg_color = "#f0f0f0"
        self.primary_color = "#4CAF50"
        self.danger_color = "#f44336"
        self.warning_color = "#ff9800"
        self.info_color = "#2196F3"
        
        self.root.configure(bg=self.bg_color)
        
        # Configure styles
        self.setup_styles()
        
        # Create UI components
        self.create_widgets()
        
        # Load and display tasks
        self.refresh_task_list()
        
        # Update statistics
        self.update_statistics()
    
    def setup_styles(self):
        """Configure ttk styles for widgets."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure Treeview style
        style.configure("Treeview",
                       background="white",
                       foreground="black",
                       rowheight=30,
                       fieldbackground="white",
                       borderwidth=0)
        
        style.map('Treeview', background=[('selected', self.info_color)])
        
        style.configure("Treeview.Heading",
                       background=self.primary_color,
                       foreground="white",
                       relief="flat",
                       font=('Arial', 10, 'bold'))
        
        style.map("Treeview.Heading",
                 background=[('active', '#45a049')])
    
    def create_widgets(self):
        """Create and layout all GUI widgets."""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ===== HEADER =====
        header_frame = tk.Frame(main_frame, bg=self.primary_color, height=80)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame,
                               text="📝 To-Do List Manager",
                               font=("Arial", 24, "bold"),
                               bg=self.primary_color,
                               fg="white")
        title_label.pack(pady=20)
        
        # ===== INPUT SECTION =====
        input_frame = tk.Frame(main_frame, bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Task input field
        self.task_entry = tk.Entry(input_frame,
                                   font=("Arial", 12),
                                   relief=tk.SOLID,
                                   borderwidth=1)
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
        self.task_entry.insert(0, "Enter a new task...")
        self.task_entry.config(fg="gray")
        
        # Placeholder functionality
        self.task_entry.bind("<FocusIn>", self.on_entry_click)
        self.task_entry.bind("<FocusOut>", self.on_focus_out)
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        # Add button
        add_button = tk.Button(input_frame,
                              text="➕ Add Task",
                              font=("Arial", 11, "bold"),
                              bg=self.primary_color,
                              fg="white",
                              relief=tk.FLAT,
                              cursor="hand2",
                              command=self.add_task,
                              padx=20)
        add_button.pack(side=tk.LEFT, padx=(10, 0), ipady=8)
        
        # ===== FILTER SECTION =====
        filter_frame = tk.Frame(main_frame, bg=self.bg_color)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        filter_label = tk.Label(filter_frame,
                               text="Filter:",
                               font=("Arial", 10, "bold"),
                               bg=self.bg_color)
        filter_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.filter_var = tk.StringVar(value="all")
        
        filters = [
            ("All Tasks", "all"),
            ("Pending", "pending"),
            ("Completed", "completed")
        ]
        
        for text, value in filters:
            rb = tk.Radiobutton(filter_frame,
                               text=text,
                               variable=self.filter_var,
                               value=value,
                               font=("Arial", 10),
                               bg=self.bg_color,
                               command=self.refresh_task_list,
                               cursor="hand2")
            rb.pack(side=tk.LEFT, padx=5)
        
        # ===== TASK LIST =====
        list_frame = tk.Frame(main_frame, bg="white", relief=tk.SOLID, borderwidth=1)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview for task list
        columns = ("ID", "Title", "Status", "Updated")
        self.task_tree = ttk.Treeview(list_frame,
                                      columns=columns,
                                      show="headings",
                                      yscrollcommand=scrollbar.set,
                                      selectmode="browse")
        
        # Configure columns
        self.task_tree.heading("ID", text="ID")
        self.task_tree.heading("Title", text="Task Title")
        self.task_tree.heading("Status", text="Status")
        self.task_tree.heading("Updated", text="Last Updated")
        
        self.task_tree.column("ID", width=50, anchor=tk.CENTER)
        self.task_tree.column("Title", width=400, anchor=tk.W)
        self.task_tree.column("Status", width=100, anchor=tk.CENTER)
        self.task_tree.column("Updated", width=150, anchor=tk.CENTER)
        
        self.task_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_tree.yview)
        
        # Double-click to toggle status
        self.task_tree.bind("<Double-1>", lambda e: self.toggle_task_status())
        
        # ===== BUTTON PANEL =====
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        buttons = [
            ("✏️ Edit", self.edit_task, self.info_color),
            ("✓ Mark Complete", self.mark_as_completed, self.primary_color),
            ("↺ Mark Pending", self.mark_as_pending, self.warning_color),
            ("🗑️ Delete", self.delete_task, self.danger_color),
            ("🗑️ Clear Completed", self.clear_completed, self.danger_color),
            ("🔄 Refresh", self.refresh_task_list, self.info_color)
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(button_frame,
                           text=text,
                           font=("Arial", 10, "bold"),
                           bg=color,
                           fg="white",
                           relief=tk.FLAT,
                           cursor="hand2",
                           command=command,
                           padx=15,
                           pady=8)
            btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # ===== STATISTICS PANEL =====
        stats_frame = tk.Frame(main_frame, bg="white", relief=tk.SOLID, borderwidth=1)
        stats_frame.pack(fill=tk.X)
        
        self.stats_label = tk.Label(stats_frame,
                                    text="Total: 0 | Completed: 0 | Pending: 0",
                                    font=("Arial", 11),
                                    bg="white",
                                    fg="#333",
                                    pady=10)
        self.stats_label.pack()
    
    def on_entry_click(self, event):
        """Handle entry field focus in (remove placeholder)."""
        if self.task_entry.get() == "Enter a new task...":
            self.task_entry.delete(0, tk.END)
            self.task_entry.config(fg="black")
    
    def on_focus_out(self, event):
        """Handle entry field focus out (restore placeholder if empty)."""
        if not self.task_entry.get():
            self.task_entry.insert(0, "Enter a new task...")
            self.task_entry.config(fg="gray")
    
    def get_selected_task_id(self) -> Optional[int]:
        """
        Get the ID of the currently selected task.
        
        Returns:
            int: Task ID if a task is selected, None otherwise
        """
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a task first!")
            return None
        
        item = self.task_tree.item(selection[0])
        return int(item['values'][0])
    
    def refresh_task_list(self):
        """Refresh the task list display based on current filter."""
        # Clear existing items
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Get tasks based on filter
        all_tasks = self.manager.get_all_tasks()
        filter_value = self.filter_var.get()
        
        if filter_value == "pending":
            tasks = [t for t in all_tasks if not t.completed]
        elif filter_value == "completed":
            tasks = [t for t in all_tasks if t.completed]
        else:
            tasks = all_tasks
        
        # Add tasks to treeview
        for task in tasks:
            status = "✓ Completed" if task.completed else "⏳ Pending"
            tag = "completed" if task.completed else "pending"
            
            self.task_tree.insert("", tk.END,
                                 values=(task.id, task.title, status, task.updated_at),
                                 tags=(tag,))
        
        # Configure row colors
        self.task_tree.tag_configure("completed", foreground="gray")
        self.task_tree.tag_configure("pending", foreground="black")
        
        # Update statistics
        self.update_statistics()
    
    def update_statistics(self):
        """Update the statistics display."""
        stats = self.manager.get_task_count()
        self.stats_label.config(
            text=f"Total: {stats['total']} | Completed: {stats['completed']} | Pending: {stats['pending']}"
        )
    
    def add_task(self):
        """Add a new task from the entry field."""
        title = self.task_entry.get()
        
        # Check if placeholder text
        if title == "Enter a new task..." or not title.strip():
            messagebox.showwarning("Empty Task", "Please enter a task title!")
            return
        
        # Add task
        task = self.manager.add_task(title)
        
        if task:
            # Clear entry field
            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(0, "Enter a new task...")
            self.task_entry.config(fg="gray")
            
            # Refresh display
            self.refresh_task_list()
            
            # Show success message
            messagebox.showinfo("Success", f"Task added successfully!\nID: {task.id}")
    
    def edit_task(self):
        """Edit the selected task."""
        task_id = self.get_selected_task_id()
        if not task_id:
            return
        
        task = self.manager.get_task_by_id(task_id)
        if not task:
            messagebox.showerror("Error", "Task not found!")
            return
        
        # Get new title from user
        new_title = simpledialog.askstring(
            "Edit Task",
            "Enter new task title:",
            initialvalue=task.title,
            parent=self.root
        )
        
        if new_title and new_title.strip():
            if self.manager.update_task(task_id, new_title):
                self.refresh_task_list()
                messagebox.showinfo("Success", "Task updated successfully!")
    
    def toggle_task_status(self):
        """Toggle the completion status of the selected task."""
        task_id = self.get_selected_task_id()
        if not task_id:
            return
        
        if self.manager.toggle_task_status(task_id):
            self.refresh_task_list()
    
    def mark_as_completed(self):
        """Mark the selected task as completed."""
        task_id = self.get_selected_task_id()
        if not task_id:
            return
        
        if self.manager.set_task_status(task_id, completed=True):
            self.refresh_task_list()
            messagebox.showinfo("Success", "Task marked as completed!")
    
    def mark_as_pending(self):
        """Mark the selected task as pending."""
        task_id = self.get_selected_task_id()
        if not task_id:
            return
        
        if self.manager.set_task_status(task_id, completed=False):
            self.refresh_task_list()
            messagebox.showinfo("Success", "Task marked as pending!")
    
    def delete_task(self):
        """Delete the selected task."""
        task_id = self.get_selected_task_id()
        if not task_id:
            return
        
        task = self.manager.get_task_by_id(task_id)
        if not task:
            messagebox.showerror("Error", "Task not found!")
            return
        
        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete this task?\n\n{task.title}"
        )
        
        if confirm:
            if self.manager.delete_task(task_id):
                self.refresh_task_list()
                messagebox.showinfo("Success", "Task deleted successfully!")
    
    def clear_completed(self):
        """Delete all completed tasks."""
        stats = self.manager.get_task_count()
        
        if stats['completed'] == 0:
            messagebox.showinfo("No Tasks", "No completed tasks to delete!")
            return
        
        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete {stats['completed']} completed task(s)?"
        )
        
        if confirm:
            count = self.manager.clear_completed_tasks()
            self.refresh_task_list()
            messagebox.showinfo("Success", f"Deleted {count} completed task(s)!")
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


def main():
    """Entry point for the GUI application."""
    root = tk.Tk()
    app = TodoGUI(root)
    app.run()


if __name__ == "__main__":
    main()

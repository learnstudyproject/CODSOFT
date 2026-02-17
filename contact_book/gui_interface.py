"""
Contact Management System - Graphical User Interface
This module provides a Tkinter-based GUI for managing contacts.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from contact_manager import ContactManager

class ContactApp:
    """Main GUI Application Class"""
    
    def __init__(self, root):
        """Initialize the GUI application"""
        self.root = root
        self.root.title("📇 Contact Management System")
        self.root.geometry("900x650")
        self.root.resizable(False, False)
        
        # Initialize ContactManager
        self.manager = ContactManager()
        
        # Color scheme
        self.bg_color = "#f0f0f0"
        self.primary_color = "#4CAF50"
        self.secondary_color = "#2196F3"
        self.danger_color = "#f44336"
        self.text_color = "#212121"
        
        self.root.configure(bg=self.bg_color)
        
        # Create GUI components
        self.create_header()
        self.create_input_section()
        self.create_button_section()
        self.create_contact_list()
        self.create_status_bar()
        
        # Load and display contacts
        self.refresh_contact_list()
    
    def create_header(self):
        """Create application header"""
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="📇 CONTACT MANAGEMENT SYSTEM",
            font=("Arial", 24, "bold"),
            bg=self.primary_color,
            fg="white"
        )
        title_label.pack(pady=20)
    
    def create_input_section(self):
        """Create input fields section"""
        input_frame = tk.Frame(self.root, bg=self.bg_color)
        input_frame.pack(pady=20, padx=20, fill=tk.X)
        
        # Name field
        tk.Label(input_frame, text="📛 Full Name:", font=("Arial", 10, "bold"), 
                bg=self.bg_color, fg=self.text_color).grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = tk.Entry(input_frame, font=("Arial", 11), width=40)
        self.name_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # Phone field
        tk.Label(input_frame, text="📱 Phone Number:", font=("Arial", 10, "bold"),
                bg=self.bg_color, fg=self.text_color).grid(row=1, column=0, sticky="w", pady=5)
        self.phone_entry = tk.Entry(input_frame, font=("Arial", 11), width=40)
        self.phone_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Email field
        tk.Label(input_frame, text="📧 Email Address:", font=("Arial", 10, "bold"),
                bg=self.bg_color, fg=self.text_color).grid(row=2, column=0, sticky="w", pady=5)
        self.email_entry = tk.Entry(input_frame, font=("Arial", 11), width=40)
        self.email_entry.grid(row=2, column=1, pady=5, padx=10)
        
        # Address field
        tk.Label(input_frame, text="🏠 Address:", font=("Arial", 10, "bold"),
                bg=self.bg_color, fg=self.text_color).grid(row=3, column=0, sticky="w", pady=5)
        self.address_entry = tk.Entry(input_frame, font=("Arial", 11), width=40)
        self.address_entry.grid(row=3, column=1, pady=5, padx=10)
    
    def create_button_section(self):
        """Create action buttons section"""
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=10)
        
        # Add button
        add_btn = tk.Button(
            button_frame,
            text="➕ Add Contact",
            font=("Arial", 10, "bold"),
            bg=self.primary_color,
            fg="white",
            width=15,
            height=2,
            cursor="hand2",
            command=self.add_contact
        )
        add_btn.grid(row=0, column=0, padx=5)
        
        # Update button
        update_btn = tk.Button(
            button_frame,
            text="✏ Update Contact",
            font=("Arial", 10, "bold"),
            bg=self.secondary_color,
            fg="white",
            width=15,
            height=2,
            cursor="hand2",
            command=self.update_contact
        )
        update_btn.grid(row=0, column=1, padx=5)
        
        # Delete button
        delete_btn = tk.Button(
            button_frame,
            text="🗑 Delete Contact",
            font=("Arial", 10, "bold"),
            bg=self.danger_color,
            fg="white",
            width=15,
            height=2,
            cursor="hand2",
            command=self.delete_contact
        )
        delete_btn.grid(row=0, column=2, padx=5)
        
        # Clear button
        clear_btn = tk.Button(
            button_frame,
            text="🔄 Clear Fields",
            font=("Arial", 10, "bold"),
            bg="#757575",
            fg="white",
            width=15,
            height=2,
            cursor="hand2",
            command=self.clear_fields
        )
        clear_btn.grid(row=0, column=3, padx=5)
        
        # Search section
        search_frame = tk.Frame(self.root, bg=self.bg_color)
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="🔍 Search:", font=("Arial", 10, "bold"),
                bg=self.bg_color, fg=self.text_color).pack(side=tk.LEFT, padx=5)
        
        self.search_entry = tk.Entry(search_frame, font=("Arial", 11), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        search_btn = tk.Button(
            search_frame,
            text="Search",
            font=("Arial", 10),
            bg="#FF9800",
            fg="white",
            cursor="hand2",
            command=self.search_contacts
        )
        search_btn.pack(side=tk.LEFT, padx=5)
        
        show_all_btn = tk.Button(
            search_frame,
            text="Show All",
            font=("Arial", 10),
            bg="#607D8B",
            fg="white",
            cursor="hand2",
            command=self.refresh_contact_list
        )
        show_all_btn.pack(side=tk.LEFT, padx=5)
    
    def create_contact_list(self):
        """Create contact list display using Treeview"""
        list_frame = tk.Frame(self.root, bg=self.bg_color)
        list_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Create Treeview
        columns = ("Name", "Phone", "Email", "Address")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        # Define headings
        self.tree.heading("Name", text="📛 Name")
        self.tree.heading("Phone", text="📱 Phone")
        self.tree.heading("Email", text="📧 Email")
        self.tree.heading("Address", text="🏠 Address")
        
        # Define column widths
        self.tree.column("Name", width=180)
        self.tree.column("Phone", width=150)
        self.tree.column("Email", width=200)
        self.tree.column("Address", width=250)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_contact_select)
    
    def create_status_bar(self):
        """Create status bar to show contact count"""
        self.status_bar = tk.Label(
            self.root,
            text="Total Contacts: 0",
            font=("Arial", 10),
            bg=self.primary_color,
            fg="white",
            anchor="w",
            relief=tk.SUNKEN
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def refresh_contact_list(self):
        """Refresh the contact list display"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get all contacts
        contacts = self.manager.view_all_contacts()
        
        # Add contacts to tree
        for contact in contacts:
            self.tree.insert("", tk.END, values=(
                contact['name'],
                contact['phone'],
                contact['email'],
                contact['address']
            ))
        
        # Update status bar
        self.status_bar.config(text=f"Total Contacts: {len(contacts)}")
    
    def clear_fields(self):
        """Clear all input fields"""
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)
    
    def add_contact(self):
        """Add a new contact"""
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()
        
        if not all([name, phone, email, address]):
            messagebox.showwarning("Missing Information", "Please fill in all fields!")
            return
        
        success, message = self.manager.add_contact(name, phone, email, address)
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_fields()
            self.refresh_contact_list()
        else:
            messagebox.showerror("Error", message)
    
    def on_contact_select(self, event):
        """Handle contact selection from list"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            # Populate input fields with selected contact
            self.clear_fields()
            self.name_entry.insert(0, values[0])
            self.phone_entry.insert(0, values[1])
            self.email_entry.insert(0, values[2])
            self.address_entry.insert(0, values[3])
    
    def update_contact(self):
        """Update selected contact"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a contact to update!")
            return
        
        # Get current values from tree
        item = self.tree.item(selection[0])
        old_values = item['values']
        old_phone = old_values[1]  # Use phone as identifier
        
        # Get new values from entries
        new_name = self.name_entry.get().strip()
        new_phone = self.phone_entry.get().strip()
        new_email = self.email_entry.get().strip()
        new_address = self.address_entry.get().strip()
        
        if not all([new_name, new_phone, new_email, new_address]):
            messagebox.showwarning("Missing Information", "Please fill in all fields!")
            return
        
        # Check if anything changed
        if (new_name == old_values[0] and new_phone == old_values[1] and 
            new_email == old_values[2] and new_address == old_values[3]):
            messagebox.showinfo("No Changes", "No changes detected!")
            return
        
        success, message = self.manager.update_contact(
            old_phone, new_name, new_phone, new_email, new_address
        )
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_fields()
            self.refresh_contact_list()
        else:
            messagebox.showerror("Error", message)
    
    def delete_contact(self):
        """Delete selected contact"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a contact to delete!")
            return
        
        # Get contact details
        item = self.tree.item(selection[0])
        values = item['values']
        name = values[0]
        phone = values[1]
        
        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete contact:\n\n{name}\n{phone}?"
        )
        
        if confirm:
            success, message, deleted = self.manager.delete_contact(phone)
            
            if success:
                messagebox.showinfo("Success", message)
                self.clear_fields()
                self.refresh_contact_list()
            else:
                messagebox.showerror("Error", message)
    
    def search_contacts(self):
        """Search contacts by query"""
        query = self.search_entry.get().strip()
        
        if not query:
            messagebox.showwarning("Empty Search", "Please enter a search query!")
            return
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Search and display results
        results = self.manager.search_contacts(query)
        
        if not results:
            messagebox.showinfo("No Results", f"No contacts found matching '{query}'")
            self.refresh_contact_list()
        else:
            for contact in results:
                self.tree.insert("", tk.END, values=(
                    contact['name'],
                    contact['phone'],
                    contact['email'],
                    contact['address']
                ))
            
            self.status_bar.config(text=f"Found {len(results)} contact(s)")

def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

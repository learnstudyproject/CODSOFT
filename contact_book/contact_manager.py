

import json
import re
import os
from typing import List, Dict, Optional

# Constants
CONTACTS_FILE = "contacts.json"

class ContactManager:
    """Main class to manage all contact operations"""
    
    def __init__(self):
        """Initialize the ContactManager and load existing contacts"""
        self.contacts = []
        self.load_contacts()
    
    def load_contacts(self):
        """Load contacts from JSON file"""
        try:
            if os.path.exists(CONTACTS_FILE):
                with open(CONTACTS_FILE, 'r') as file:
                    self.contacts = json.load(file)
                print(f"✓ Loaded {len(self.contacts)} contacts successfully.")
            else:
                print("✓ Starting with empty contact list.")
                self.contacts = []
        except json.JSONDecodeError:
            print("⚠ Warning: Corrupted contacts file. Starting fresh.")
            self.contacts = []
        except Exception as e:
            print(f"⚠ Error loading contacts: {e}")
            self.contacts = []
    
    def save_contacts(self):
        """Save contacts to JSON file"""
        try:
            with open(CONTACTS_FILE, 'w') as file:
                json.dump(self.contacts, file, indent=4)
            return True
        except Exception as e:
            print(f"✗ Error saving contacts: {e}")
            return False
    
    @staticmethod
    def validate_name(name: str) -> bool:
        """Validate contact name (non-empty, alphabetic with spaces)"""
        if not name or not name.strip():
            return False
        # Allow letters, spaces, hyphens, and apostrophes
        return bool(re.match(r"^[A-Za-z\s\-']+$", name.strip()))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number (10-15 digits, may include +, spaces, hyphens)"""
        if not phone or not phone.strip():
            return False
        # Remove spaces, hyphens, and parentheses for validation
        cleaned = re.sub(r'[\s\-()]', '', phone)
        # Check if it starts with + and has 10-15 digits
        if cleaned.startswith('+'):
            return bool(re.match(r'^\+\d{10,15}$', cleaned))
        # Or just 10-15 digits
        return bool(re.match(r'^\d{10,15}$', cleaned))
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email address format"""
        if not email or not email.strip():
            return False
        # Basic email validation pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email.strip()))
    
    @staticmethod
    def validate_address(address: str) -> bool:
        """Validate address (just check if not empty)"""
        return bool(address and address.strip())
    
    def add_contact(self, name: str, phone: str, email: str, address: str) -> tuple:
        """
        Add a new contact to the system
        Returns: (success: bool, message: str)
        """
        # Validate all fields
        if not self.validate_name(name):
            return False, "✗ Invalid name. Use only letters, spaces, hyphens, and apostrophes."
        
        if not self.validate_phone(phone):
            return False, "✗ Invalid phone number. Use 10-15 digits (may include + prefix)."
        
        if not self.validate_email(email):
            return False, "✗ Invalid email format. Example: user@example.com"
        
        if not self.validate_address(address):
            return False, "✗ Invalid address. Address cannot be empty."
        
        # Check for duplicate phone or email
        for contact in self.contacts:
            if contact['phone'] == phone.strip():
                return False, f"✗ Contact with phone {phone} already exists!"
            if contact['email'].lower() == email.strip().lower():
                return False, f"✗ Contact with email {email} already exists!"
        
        # Create new contact
        new_contact = {
            'name': name.strip().title(),
            'phone': phone.strip(),
            'email': email.strip().lower(),
            'address': address.strip()
        }
        
        self.contacts.append(new_contact)
        
        # Save to file
        if self.save_contacts():
            return True, f"✓ Contact '{new_contact['name']}' added successfully!"
        else:
            return False, "✗ Failed to save contact."
    
    def view_all_contacts(self) -> List[Dict]:
        """Return all contacts"""
        return self.contacts
    
    def search_contacts(self, query: str) -> List[Dict]:
        """
        Search contacts by name or phone number
        Returns: List of matching contacts
        """
        query = query.strip().lower()
        results = []
        
        for contact in self.contacts:
            # Search in name or phone
            if (query in contact['name'].lower() or 
                query in contact['phone']):
                results.append(contact)
        
        return results
    
    def find_contact_index(self, identifier: str) -> Optional[int]:
        """
        Find contact index by phone or email
        Returns: index if found, None otherwise
        """
        identifier = identifier.strip().lower()
        
        for i, contact in enumerate(self.contacts):
            if (contact['phone'] == identifier or 
                contact['email'].lower() == identifier):
                return i
        
        return None
    
    def update_contact(self, identifier: str, name: str = None, 
                      phone: str = None, email: str = None, 
                      address: str = None) -> tuple:
        """
        Update an existing contact
        identifier: phone or email to find the contact
        Returns: (success: bool, message: str)
        """
        index = self.find_contact_index(identifier)
        
        if index is None:
            return False, "✗ Contact not found!"
        
        contact = self.contacts[index]
        
        # Validate and update fields if provided
        if name is not None:
            if not self.validate_name(name):
                return False, "✗ Invalid name format."
            contact['name'] = name.strip().title()
        
        if phone is not None:
            if not self.validate_phone(phone):
                return False, "✗ Invalid phone number format."
            # Check if new phone already exists in another contact
            for i, c in enumerate(self.contacts):
                if i != index and c['phone'] == phone.strip():
                    return False, "✗ Phone number already exists for another contact!"
            contact['phone'] = phone.strip()
        
        if email is not None:
            if not self.validate_email(email):
                return False, "✗ Invalid email format."
            # Check if new email already exists in another contact
            for i, c in enumerate(self.contacts):
                if i != index and c['email'].lower() == email.strip().lower():
                    return False, "✗ Email already exists for another contact!"
            contact['email'] = email.strip().lower()
        
        if address is not None:
            if not self.validate_address(address):
                return False, "✗ Invalid address."
            contact['address'] = address.strip()
        
        # Save changes
        if self.save_contacts():
            return True, f"✓ Contact '{contact['name']}' updated successfully!"
        else:
            return False, "✗ Failed to save changes."
    
    def delete_contact(self, identifier: str) -> tuple:
        """
        Delete a contact by phone or email
        Returns: (success: bool, message: str, deleted_contact: dict or None)
        """
        index = self.find_contact_index(identifier)
        
        if index is None:
            return False, "✗ Contact not found!", None
        
        deleted_contact = self.contacts.pop(index)
        
        # Save changes
        if self.save_contacts():
            return True, f"✓ Contact '{deleted_contact['name']}' deleted successfully!", deleted_contact
        else:
            # Restore the contact if save failed
            self.contacts.insert(index, deleted_contact)
            return False, "✗ Failed to delete contact.", None
    
    def get_contact_count(self) -> int:
        """Return total number of contacts"""
        return len(self.contacts)

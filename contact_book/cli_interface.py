

from contact_manager import ContactManager
import os

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print application header"""
    print("=" * 60)
    print(" " * 15 + "📇 CONTACT MANAGEMENT SYSTEM 📇")
    print("=" * 60)

def print_menu():
    """Display main menu options"""
    print("\n📋 MAIN MENU:")
    print("-" * 60)
    print("  1. ➕ Add New Contact")
    print("  2. 👁  View All Contacts")
    print("  3. 🔍 Search Contact")
    print("  4. ✏  Update Contact")
    print("  5. 🗑  Delete Contact")
    print("  6. 📊 Contact Statistics")
    print("  0. 🚪 Exit")
    print("-" * 60)

def print_contact(contact, index=None):
    """Print a single contact in formatted style"""
    if index is not None:
        print(f"\n{'─' * 60}")
        print(f"Contact #{index + 1}")
    print(f"{'─' * 60}")
    print(f"📛 Name    : {contact['name']}")
    print(f"📱 Phone   : {contact['phone']}")
    print(f"📧 Email   : {contact['email']}")
    print(f"🏠 Address : {contact['address']}")
    print(f"{'─' * 60}")

def add_contact_ui(manager):
    """UI for adding a new contact"""
    clear_screen()
    print_header()
    print("\n➕ ADD NEW CONTACT")
    print("=" * 60)
    
    # Get contact details
    name = input("Enter Full Name: ").strip()
    phone = input("Enter Phone Number: ").strip()
    email = input("Enter Email Address: ").strip()
    address = input("Enter Address: ").strip()
    
    # Add contact
    success, message = manager.add_contact(name, phone, email, address)
    print(f"\n{message}")
    
    input("\nPress Enter to continue...")

def view_all_contacts_ui(manager):
    """UI for viewing all contacts"""
    clear_screen()
    print_header()
    print("\n👁  ALL CONTACTS")
    print("=" * 60)
    
    contacts = manager.view_all_contacts()
    
    if not contacts:
        print("\n⚠ No contacts found. Your contact list is empty!")
    else:
        print(f"\nTotal Contacts: {len(contacts)}\n")
        for i, contact in enumerate(contacts):
            print_contact(contact, i)
    
    input("\nPress Enter to continue...")

def search_contact_ui(manager):
    """UI for searching contacts"""
    clear_screen()
    print_header()
    print("\n🔍 SEARCH CONTACT")
    print("=" * 60)
    
    query = input("\nEnter name or phone number to search: ").strip()
    
    if not query:
        print("\n⚠ Search query cannot be empty!")
    else:
        results = manager.search_contacts(query)
        
        if not results:
            print(f"\n⚠ No contacts found matching '{query}'")
        else:
            print(f"\n✓ Found {len(results)} contact(s):\n")
            for i, contact in enumerate(results):
                print_contact(contact, i)
    
    input("\nPress Enter to continue...")

def update_contact_ui(manager):
    """UI for updating a contact"""
    clear_screen()
    print_header()
    print("\n✏  UPDATE CONTACT")
    print("=" * 60)
    
    identifier = input("\nEnter phone or email of contact to update: ").strip()
    
    # Find and display current contact
    index = manager.find_contact_index(identifier)
    
    if index is None:
        print("\n✗ Contact not found!")
    else:
        current = manager.contacts[index]
        print("\n📄 Current Contact Details:")
        print_contact(current)
        
        print("\n✏  Enter new details (press Enter to keep current value):")
        print("-" * 60)
        
        # Get new values
        name = input(f"New Name [{current['name']}]: ").strip()
        phone = input(f"New Phone [{current['phone']}]: ").strip()
        email = input(f"New Email [{current['email']}]: ").strip()
        address = input(f"New Address [{current['address']}]: ").strip()
        
        # Only update if values provided
        name = name if name else None
        phone = phone if phone else None
        email = email if email else None
        address = address if address else None
        
        # Check if any changes made
        if not any([name, phone, email, address]):
            print("\n⚠ No changes made.")
        else:
            success, message = manager.update_contact(identifier, name, phone, email, address)
            print(f"\n{message}")
    
    input("\nPress Enter to continue...")

def delete_contact_ui(manager):
    """UI for deleting a contact"""
    clear_screen()
    print_header()
    print("\n🗑  DELETE CONTACT")
    print("=" * 60)
    
    identifier = input("\nEnter phone or email of contact to delete: ").strip()
    
    # Find and display contact
    index = manager.find_contact_index(identifier)
    
    if index is None:
        print("\n✗ Contact not found!")
    else:
        contact = manager.contacts[index]
        print("\n📄 Contact to be deleted:")
        print_contact(contact)
        
        # Confirm deletion
        confirmation = input("\n⚠ Are you sure you want to delete this contact? (yes/no): ").strip().lower()
        
        if confirmation in ['yes', 'y']:
            success, message, deleted = manager.delete_contact(identifier)
            print(f"\n{message}")
        else:
            print("\n✓ Deletion cancelled.")
    
    input("\nPress Enter to continue...")

def show_statistics_ui(manager):
    """UI for showing contact statistics"""
    clear_screen()
    print_header()
    print("\n📊 CONTACT STATISTICS")
    print("=" * 60)
    
    total = manager.get_contact_count()
    contacts = manager.view_all_contacts()
    
    print(f"\n📈 Total Contacts: {total}")
    
    if total > 0:
        # Count domains
        domains = {}
        for contact in contacts:
            domain = contact['email'].split('@')[1] if '@' in contact['email'] else 'unknown'
            domains[domain] = domains.get(domain, 0) + 1
        
        print(f"\n📧 Email Domains:")
        for domain, count in sorted(domains.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {domain}: {count} contact(s)")
        
        # Show recent contacts
        print(f"\n📝 Recent Contacts (Last 5):")
        for i, contact in enumerate(contacts[-5:][::-1], 1):
            print(f"   {i}. {contact['name']} - {contact['phone']}")
    
    input("\nPress Enter to continue...")

def main():
    """Main function to run the CLI application"""
    # Initialize contact manager
    manager = ContactManager()
    
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        choice = input("\n👉 Enter your choice (0-6): ").strip()
        
        if choice == '1':
            add_contact_ui(manager)
        elif choice == '2':
            view_all_contacts_ui(manager)
        elif choice == '3':
            search_contact_ui(manager)
        elif choice == '4':
            update_contact_ui(manager)
        elif choice == '5':
            delete_contact_ui(manager)
        elif choice == '6':
            show_statistics_ui(manager)
        elif choice == '0':
            clear_screen()
            print_header()
            print("\n👋 Thank you for using Contact Management System!")
            print("    Goodbye! 🌟\n")
            print("=" * 60)
            break
        else:
            print("\n✗ Invalid choice! Please enter a number between 0 and 6.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()

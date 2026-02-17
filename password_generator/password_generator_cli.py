

import secrets
import string


def display_header():
    """Display the application header."""
    print("\n" + "=" * 60)
    print(" " * 15 + "PASSWORD GENERATOR")
    print("=" * 60)


def display_menu():
    """Display the main menu options."""
    print("\n📋 MAIN MENU:")
    print("1. Generate Password")
    print("2. Help & Information")
    print("3. Exit")
    print("-" * 60)


def get_password_length():
    """
    Prompt user for desired password length with validation.
    
    Returns:
        int: Valid password length (minimum 4, maximum 128)
    
    Raises:
        ValueError: If input is not a valid integer
    """
    while True:
        try:
            length = input("\n🔢 Enter password length (4-128): ").strip()
            
            # Check if input is empty
            if not length:
                print("❌ Error: Password length cannot be empty!")
                continue
            
            # Convert to integer
            length = int(length)
            
            # Validate range
            if length < 4:
                print("❌ Error: Password length must be at least 4 characters!")
                continue
            elif length > 128:
                print("❌ Error: Password length cannot exceed 128 characters!")
                continue
            
            return length
            
        except ValueError:
            print("❌ Error: Please enter a valid number!")


def get_password_options():
    """
    Get password complexity options from user.
    
    Returns:
        dict: Dictionary containing boolean values for each character type
    
    The function ensures at least one option is selected.
    """
    print("\n🔐 PASSWORD COMPLEXITY OPTIONS:")
    print("(Press 'y' for Yes or 'n' for No)")
    print("-" * 60)
    
    while True:
        options = {}
        
        # Get each option
        options['uppercase'] = get_yes_no_input("Include UPPERCASE letters (A-Z)?")
        options['lowercase'] = get_yes_no_input("Include lowercase letters (a-z)?")
        options['numbers'] = get_yes_no_input("Include numbers (0-9)?")
        options['special'] = get_yes_no_input("Include special characters (!@#$%...)?")
        
        # Validate that at least one option is selected
        if not any(options.values()):
            print("\n❌ Error: You must select at least ONE option!")
            print("Please try again...\n")
            continue
        
        return options


def get_yes_no_input(prompt):
    """
    Get yes/no input from user with validation.
    
    Args:
        prompt (str): The question to ask the user
    
    Returns:
        bool: True for 'yes', False for 'no'
    """
    while True:
        choice = input(f"   {prompt} (y/n): ").strip().lower()
        
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("   ❌ Invalid input! Please enter 'y' or 'n'.")


def generate_password(length, options):
    """
    Generate a secure random password based on specified options.
    
    Args:
        length (int): Desired length of the password
        options (dict): Dictionary of character type options
    
    Returns:
        str: Generated secure password
    
    This function uses the 'secrets' module which is designed for
    cryptographically strong random generation, making it suitable
    for security-sensitive applications like password generation.
    """
    # Build character pool based on selected options
    char_pool = ""
    
    if options['uppercase']:
        char_pool += string.ascii_uppercase  # A-Z
    
    if options['lowercase']:
        char_pool += string.ascii_lowercase  # a-z
    
    if options['numbers']:
        char_pool += string.digits  # 0-9
    
    if options['special']:
        char_pool += string.punctuation  # !@#$%^&*()...
    
    # Generate password using secrets module for security
    # secrets.choice() is cryptographically strong
    password = ''.join(secrets.choice(char_pool) for _ in range(length))
    
    return password


def display_password(password, options):
    """
    Display the generated password with formatting.
    
    Args:
        password (str): The generated password
        options (dict): Dictionary of character type options used
    """
    print("\n" + "=" * 60)
    print("✅ PASSWORD GENERATED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\n🔑 Your Password: {password}")
    print(f"\n📊 Password Length: {len(password)} characters")
    
    print("\n📋 Included Character Types:")
    if options['uppercase']:
        print("   ✓ Uppercase letters (A-Z)")
    if options['lowercase']:
        print("   ✓ Lowercase letters (a-z)")
    if options['numbers']:
        print("   ✓ Numbers (0-9)")
    if options['special']:
        print("   ✓ Special characters (!@#$%...)")
    
    print("\n" + "=" * 60)
    print("💡 Tip: Store your password in a secure password manager!")
    print("=" * 60)


def display_help():
    """Display help information about password security."""
    print("\n" + "=" * 60)
    print(" " * 18 + "HELP & INFORMATION")
    print("=" * 60)
    
    print("\n🔐 What makes a strong password?")
    print("-" * 60)
    print("1. Length: At least 12-16 characters (longer is better)")
    print("2. Complexity: Mix of uppercase, lowercase, numbers, and symbols")
    print("3. Unpredictability: Avoid common words, patterns, or personal info")
    print("4. Uniqueness: Use different passwords for different accounts")
    
    print("\n💡 Password Security Tips:")
    print("-" * 60)
    print("• Never share your password with anyone")
    print("• Use a password manager to store passwords securely")
    print("• Enable two-factor authentication when available")
    print("• Change passwords regularly (every 3-6 months)")
    print("• Avoid using the same password across multiple sites")
    
    print("\n🛡️ This Generator:")
    print("-" * 60)
    print("• Uses 'secrets' module for cryptographic security")
    print("• Generates truly random passwords")
    print("• Allows full customization of character types")
    print("• Supports passwords from 4 to 128 characters")
    
    print("\n" + "=" * 60)


def generate_password_workflow():
    """Main workflow for password generation."""
    # Get password length
    length = get_password_length()
    
    # Get complexity options
    options = get_password_options()
    
    # Generate password
    password = generate_password(length, options)
    
    # Display the result
    display_password(password, options)
    
    # Ask if user wants to generate another
    print("\n")
    while True:
        choice = input("🔄 Generate another password? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            generate_password_workflow()
            break
        elif choice in ['n', 'no']:
            break
        else:
            print("❌ Invalid input! Please enter 'y' or 'n'.")


def main():
    """
    Main function to run the Password Generator CLI application.
    
    This function provides a menu-driven interface for the user to:
    1. Generate passwords with custom options
    2. View help and security information
    3. Exit the application
    """
    display_header()
    
    while True:
        display_menu()
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            # Generate Password
            generate_password_workflow()
            
        elif choice == '2':
            # Display Help
            display_help()
            
        elif choice == '3':
            # Exit
            print("\n" + "=" * 60)
            print("👋 Thank you for using Password Generator!")
            print("   Stay secure! 🔒")
            print("=" * 60 + "\n")
            break
            
        else:
            print("\n❌ Invalid choice! Please select 1, 2, or 3.")


# Entry point of the program
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Program interrupted by user.")
        print("Exiting safely... Goodbye! 👋\n")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print("Please report this issue if it persists.\n")

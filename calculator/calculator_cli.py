
def add(num1, num2):
    """
    Add two numbers together.
    
    Parameters:
        num1 (float): First number
        num2 (float): Second number
    
    Returns:
        float: Sum of num1 and num2
    """
    return num1 + num2


def subtract(num1, num2):
    """
    Subtract the second number from the first.
    
    Parameters:
        num1 (float): First number
        num2 (float): Second number
    
    Returns:
        float: Difference of num1 and num2
    """
    return num1 - num2


def multiply(num1, num2):
    """
    Multiply two numbers.
    
    Parameters:
        num1 (float): First number
        num2 (float): Second number
    
    Returns:
        float: Product of num1 and num2
    """
    return num1 * num2


def divide(num1, num2):
    """
    Divide the first number by the second.
    
    Parameters:
        num1 (float): First number (dividend)
        num2 (float): Second number (divisor)
    
    Returns:
        float: Quotient of num1 and num2
    
    Raises:
        ZeroDivisionError: If num2 is zero
    """
    if num2 == 0:
        raise ZeroDivisionError("Cannot divide by zero!")
    return num1 / num2


def get_number_input(prompt):
    """
    Get a valid number input from the user.
    
    Parameters:
        prompt (str): Message to display to the user
    
    Returns:
        float: Valid number entered by user
    """
    while True:
        try:
            # Get input from user and convert to float
            number = float(input(prompt))
            return number
        except ValueError:
            # If conversion fails, show error and ask again
            print("❌ Invalid input! Please enter a valid number.")


def get_operation_choice():
    """
    Display operation menu and get user's choice.
    
    Returns:
        str: Valid operation choice (1, 2, 3, or 4)
    """
    print("\n" + "="*50)
    print("SELECT AN OPERATION:")
    print("="*50)
    print("1. Addition (+)")
    print("2. Subtraction (−)")
    print("3. Multiplication (×)")
    print("4. Division (÷)")
    print("="*50)
    
    # List of valid choices
    valid_choices = ['1', '2', '3', '4']
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice in valid_choices:
            return choice
        else:
            print("❌ Invalid choice! Please enter a number between 1 and 4.")


def perform_calculation(num1, num2, operation):
    """
    Perform the selected calculation and return the result.
    
    Parameters:
        num1 (float): First number
        num2 (float): Second number
        operation (str): Operation choice ('1', '2', '3', or '4')
    
    Returns:
        tuple: (result, operation_symbol, operation_name)
    """
    if operation == '1':
        result = add(num1, num2)
        return result, '+', 'Addition'
    
    elif operation == '2':
        result = subtract(num1, num2)
        return result, '−', 'Subtraction'
    
    elif operation == '3':
        result = multiply(num1, num2)
        return result, '×', 'Multiplication'
    
    elif operation == '4':
        try:
            result = divide(num1, num2)
            return result, '÷', 'Division'
        except ZeroDivisionError as e:
            # Return error message instead of result
            return str(e), '÷', 'Division'


def display_result(num1, num2, result, symbol, operation_name):
    """
    Display the calculation result in a formatted way.
    
    Parameters:
        num1 (float): First number
        num2 (float): Second number
        result (float/str): Calculation result or error message
        symbol (str): Operation symbol
        operation_name (str): Name of the operation
    """
    print("\n" + "="*50)
    print("CALCULATION RESULT")
    print("="*50)
    print(f"Operation: {operation_name}")
    print(f"Expression: {num1} {symbol} {num2}")
    
    # Check if result is an error message
    if isinstance(result, str):
        print(f"Result: ❌ {result}")
    else:
        print(f"Result: ✓ {result}")
    
    print("="*50)


def display_welcome():
    """Display welcome banner."""
    print("\n" + "="*50)
    print("🧮  SIMPLE CALCULATOR")
    print("="*50)
    print("Welcome! This calculator performs basic arithmetic.")
    print("="*50)



def main():
    """
    Main function that runs the calculator program.
    Controls the flow of the entire application.
    """
    # Display welcome message
    display_welcome()
    
    while True:
        # Step 1: Get the first number
        num1 = get_number_input("\n📥 Enter the first number: ")
        
        # Step 2: Get the second number
        num2 = get_number_input("📥 Enter the second number: ")
        
        # Step 3: Get operation choice
        operation = get_operation_choice()
        
        # Step 4: Perform calculation
        result, symbol, operation_name = perform_calculation(num1, num2, operation)
        
        # Step 5: Display result
        display_result(num1, num2, result, symbol, operation_name)
        
        # Step 6: Ask if user wants to continue
        print("\n" + "-"*50)
        continue_choice = input("Do you want to perform another calculation? (yes/no): ").strip().lower()
        
        if continue_choice not in ['yes', 'y']:
            print("\n" + "="*50)
            print("Thank you for using Simple Calculator! 👋")
            print("="*50 + "\n")
            break
        
        # Clear screen effect by printing new lines
        print("\n" * 2)



if __name__ == "__main__":
    """
    This block runs only when the script is executed directly,
    not when it's imported as a module.
    """
    main()

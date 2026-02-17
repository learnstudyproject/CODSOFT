

import tkinter as tk
from tkinter import messagebox
import math

class Calculator:
    """
    Main Calculator class that handles the GUI and calculation logic.
    """
    
    def __init__(self, root):
        """
        Initialize the calculator GUI.
        
        Parameters:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("🧮 Simple Calculator")
        self.root.geometry("400x550")
        self.root.resizable(False, False)
        
        # Set color scheme
        self.bg_color = "#1e1e2e"
        self.display_bg = "#2d2d44"
        self.button_bg = "#3d3d5c"
        self.button_fg = "#ffffff"
        self.operator_bg = "#6c63ff"
        self.equals_bg = "#4CAF50"
        self.clear_bg = "#f44336"
        
        # Configure root background
        self.root.configure(bg=self.bg_color)
        
        # Variables to store calculation state
        self.current_input = ""
        self.first_number = None
        self.operation = None
        self.new_number = True
        
        # Create GUI elements
        self.create_widgets()
    
    def create_widgets(self):
        """Create and layout all GUI widgets."""
       
        display_frame = tk.Frame(self.root, bg=self.bg_color, pady=20)
        display_frame.pack(fill=tk.BOTH)
        
        # Display label (shows current input/result)
        self.display = tk.Label(
            display_frame,
            text="0",
            font=("Arial", 32, "bold"),
            bg=self.display_bg,
            fg=self.button_fg,
            anchor="e",
            padx=20,
            pady=20,
            relief=tk.SUNKEN,
            bd=3
        )
        self.display.pack(fill=tk.BOTH, padx=20, pady=(0, 10))
        
        # Operation indicator (shows current operation)
        self.operation_label = tk.Label(
            display_frame,
            text="",
            font=("Arial", 12),
            bg=self.bg_color,
            fg="#888",
            anchor="e",
            padx=20
        )
        self.operation_label.pack(fill=tk.X, padx=20)
        
      
        buttons_frame = tk.Frame(self.root, bg=self.bg_color)
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Button layout: [text, row, column, columnspan, color]
        buttons = [
            # Row 1
            ('C', 0, 0, 2, self.clear_bg),
            ('⌫', 0, 2, 1, self.button_bg),
            ('÷', 0, 3, 1, self.operator_bg),
            
            # Row 2
            ('7', 1, 0, 1, self.button_bg),
            ('8', 1, 1, 1, self.button_bg),
            ('9', 1, 2, 1, self.button_bg),
            ('×', 1, 3, 1, self.operator_bg),
            
            # Row 3
            ('4', 2, 0, 1, self.button_bg),
            ('5', 2, 1, 1, self.button_bg),
            ('6', 2, 2, 1, self.button_bg),
            ('−', 2, 3, 1, self.operator_bg),
            
            # Row 4
            ('1', 3, 0, 1, self.button_bg),
            ('2', 3, 1, 1, self.button_bg),
            ('3', 3, 2, 1, self.button_bg),
            ('+', 3, 3, 1, self.operator_bg),
            
            # Row 5
            ('0', 4, 0, 2, self.button_bg),
            ('.', 4, 2, 1, self.button_bg),
            ('=', 4, 3, 1, self.equals_bg),
        ]
        
        # Create and place all buttons
        for button_text, row, col, colspan, color in buttons:
            btn = tk.Button(
                buttons_frame,
                text=button_text,
                font=("Arial", 18, "bold"),
                bg=color,
                fg=self.button_fg,
                activebackground=color,
                activeforeground=self.button_fg,
                relief=tk.RAISED,
                bd=3,
                command=lambda t=button_text: self.on_button_click(t)
            )
            btn.grid(
                row=row,
                column=col,
                columnspan=colspan,
                sticky="nsew",
                padx=5,
                pady=5
            )
        
        # Configure grid weights for responsive layout
        for i in range(5):
            buttons_frame.rowconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.columnconfigure(i, weight=1)
    
  
    def on_button_click(self, button_text):
        """
        Handle button click events.
        
        Parameters:
            button_text (str): Text of the clicked button
        """
        if button_text.isdigit() or button_text == '.':
            # Number or decimal point clicked
            self.on_number_click(button_text)
        
        elif button_text in ['+', '−', '×', '÷']:
            # Operator clicked
            self.on_operator_click(button_text)
        
        elif button_text == '=':
            # Equals clicked
            self.on_equals_click()
        
        elif button_text == 'C':
            # Clear clicked
            self.on_clear_click()
        
        elif button_text == '⌫':
            # Backspace clicked
            self.on_backspace_click()
    
    def on_number_click(self, number):
        """
        Handle number/decimal button clicks.
        
        Parameters:
            number (str): The number or decimal point clicked
        """
        # Start new number if flag is set
        if self.new_number:
            self.current_input = ""
            self.new_number = False
        
        # Prevent multiple decimal points
        if number == '.' and '.' in self.current_input:
            return
        
        # Add number to current input
        self.current_input += number
        self.update_display(self.current_input)
    
    def on_operator_click(self, operator):
        """
        Handle operator button clicks.
        
        Parameters:
            operator (str): The operator clicked (+, −, ×, ÷)
        """
        if self.current_input:
            # If there's a pending operation, calculate it first
            if self.first_number is not None and self.operation is not None:
                self.on_equals_click()
            
            # Store the first number and operation
            try:
                self.first_number = float(self.current_input)
                self.operation = operator
                self.new_number = True
                self.update_operation_label(f"{self.first_number} {operator}")
            except ValueError:
                messagebox.showerror("Error", "Invalid number format!")
    
    def on_equals_click(self):
        """Handle equals button click - perform the calculation."""
        if self.first_number is not None and self.operation is not None and self.current_input:
            try:
                second_number = float(self.current_input)
                result = self.calculate(self.first_number, second_number, self.operation)
                
                # Update display with result
                if result is not None:
                    self.update_display(str(result))
                    self.update_operation_label(
                        f"{self.first_number} {self.operation} {second_number} ="
                    )
                    
                    # Reset state
                    self.current_input = str(result)
                    self.first_number = None
                    self.operation = None
                    self.new_number = True
                
            except ValueError:
                messagebox.showerror("Error", "Invalid number format!")
            except ZeroDivisionError:
                messagebox.showerror("Error", "Cannot divide by zero!")
                self.on_clear_click()
    
    def on_clear_click(self):
        """Handle clear button click - reset calculator."""
        self.current_input = ""
        self.first_number = None
        self.operation = None
        self.new_number = True
        self.update_display("0")
        self.update_operation_label("")
    
    def on_backspace_click(self):
        """Handle backspace button click - delete last character."""
        if self.current_input and not self.new_number:
            self.current_input = self.current_input[:-1]
            self.update_display(self.current_input if self.current_input else "0")
    
    
    def calculate(self, num1, num2, operator):
        """
        Perform the calculation based on the operator.
        
        Parameters:
            num1 (float): First number
            num2 (float): Second number
            operator (str): Operation to perform
        
        Returns:
            float: Result of the calculation
        
        Raises:
            ZeroDivisionError: If division by zero is attempted
        """
        if operator == '+':
            return num1 + num2
        
        elif operator == '−':
            return num1 - num2
        
        elif operator == '×':
            return num1 * num2
        
        elif operator == '÷':
            if num2 == 0:
                raise ZeroDivisionError("Cannot divide by zero!")
            return num1 / num2
        
        return None
    
   
    def update_display(self, value):
        """
        Update the main display with a value.
        
        Parameters:
            value (str): Value to display
        """
        # Limit display length
        if len(value) > 15:
            value = value[:15]
        
        self.display.config(text=value if value else "0")
    
    def update_operation_label(self, text):
        """
        Update the operation indicator label.
        
        Parameters:
            text (str): Text to display
        """
        self.operation_label.config(text=text)



def main():
    """
    Main function to create and run the calculator application.
    """
    # Create the main window
    root = tk.Tk()
    
    # Create calculator instance
    calculator = Calculator(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Start the GUI event loop
    root.mainloop()



if __name__ == "__main__":
    """
    This block runs only when the script is executed directly.
    """
    main()

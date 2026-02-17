

import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import string


class PasswordGeneratorGUI:
    """
    Main class for Password Generator GUI application.
    
    This class creates and manages the graphical interface for generating
    secure passwords with customizable options.
    """
    
    def __init__(self, root):
        """
        Initialize the Password Generator GUI.
        
        Args:
            root: The main Tkinter window
        """
        self.root = root
        self.root.title("🔐 Secure Password Generator")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        # Configure colors
        self.bg_color = "#1e1e2e"
        self.fg_color = "#cdd6f4"
        self.accent_color = "#89b4fa"
        self.success_color = "#a6e3a1"
        self.warning_color = "#f9e2af"
        self.danger_color = "#f38ba8"
        
        # Configure root background
        self.root.configure(bg=self.bg_color)
        
        # Create GUI components
        self.create_widgets()
        
    def create_widgets(self):
        """Create and layout all GUI components."""
        
        
        header_frame = tk.Frame(self.root, bg=self.accent_color, height=80)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(
            header_frame,
            text="🔐 SECURE PASSWORD GENERATOR",
            font=("Arial", 20, "bold"),
            bg=self.accent_color,
            fg=self.bg_color
        )
        header_label.pack(pady=25)
        
       
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
       
        length_frame = tk.LabelFrame(
            main_frame,
            text=" 🔢 Password Length ",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            fg=self.fg_color,
            relief="solid",
            bd=1
        )
        length_frame.pack(fill="x", pady=(0, 15))
        
        # Length slider
        self.length_var = tk.IntVar(value=12)
        
        slider_frame = tk.Frame(length_frame, bg=self.bg_color)
        slider_frame.pack(fill="x", padx=15, pady=10)
        
        self.length_label = tk.Label(
            slider_frame,
            text="12",
            font=("Arial", 16, "bold"),
            bg=self.bg_color,
            fg=self.accent_color,
            width=4
        )
        self.length_label.pack(side="left", padx=(0, 15))
        
        self.length_slider = tk.Scale(
            slider_frame,
            from_=4,
            to=128,
            orient="horizontal",
            variable=self.length_var,
            command=self.update_length_label,
            bg=self.bg_color,
            fg=self.fg_color,
            troughcolor=self.accent_color,
            highlightthickness=0,
            bd=0,
            showvalue=False
        )
        self.length_slider.pack(side="left", fill="x", expand=True)
        
        range_label = tk.Label(
            length_frame,
            text="Range: 4 - 128 characters",
            font=("Arial", 9, "italic"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        range_label.pack(padx=15, pady=(0, 10))
        
        #  CHARACTER OPTIONS SECTION 
        options_frame = tk.LabelFrame(
            main_frame,
            text=" ⚙️ Character Options ",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            fg=self.fg_color,
            relief="solid",
            bd=1
        )
        options_frame.pack(fill="x", pady=(0, 15))
        
        # Create checkboxes for each option
        checkbox_container = tk.Frame(options_frame, bg=self.bg_color)
        checkbox_container.pack(fill="x", padx=15, pady=15)
        
        # Uppercase option
        self.uppercase_var = tk.BooleanVar(value=True)
        uppercase_check = tk.Checkbutton(
            checkbox_container,
            text="Uppercase Letters (A-Z)",
            variable=self.uppercase_var,
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.fg_color,
            selectcolor=self.bg_color,
            activebackground=self.bg_color,
            activeforeground=self.accent_color,
            highlightthickness=0
        )
        uppercase_check.pack(anchor="w", pady=5)
        
        # Lowercase option
        self.lowercase_var = tk.BooleanVar(value=True)
        lowercase_check = tk.Checkbutton(
            checkbox_container,
            text="Lowercase Letters (a-z)",
            variable=self.lowercase_var,
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.fg_color,
            selectcolor=self.bg_color,
            activebackground=self.bg_color,
            activeforeground=self.accent_color,
            highlightthickness=0
        )
        lowercase_check.pack(anchor="w", pady=5)
        
        # Numbers option
        self.numbers_var = tk.BooleanVar(value=True)
        numbers_check = tk.Checkbutton(
            checkbox_container,
            text="Numbers (0-9)",
            variable=self.numbers_var,
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.fg_color,
            selectcolor=self.bg_color,
            activebackground=self.bg_color,
            activeforeground=self.accent_color,
            highlightthickness=0
        )
        numbers_check.pack(anchor="w", pady=5)
        
        # Special characters option
        self.special_var = tk.BooleanVar(value=True)
        special_check = tk.Checkbutton(
            checkbox_container,
            text="Special Characters (!@#$%^&*...)",
            variable=self.special_var,
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.fg_color,
            selectcolor=self.bg_color,
            activebackground=self.bg_color,
            activeforeground=self.accent_color,
            highlightthickness=0
        )
        special_check.pack(anchor="w", pady=5)
        
        #  GENERATE BUTTON 
        self.generate_btn = tk.Button(
            main_frame,
            text="🎲 GENERATE PASSWORD",
            command=self.generate_password,
            font=("Arial", 12, "bold"),
            bg=self.accent_color,
            fg=self.bg_color,
            activebackground=self.success_color,
            activeforeground=self.bg_color,
            relief="flat",
            cursor="hand2",
            height=2
        )
        self.generate_btn.pack(fill="x", pady=(0, 15))
        
        #  PASSWORD DISPLAY SECTION 
        display_frame = tk.LabelFrame(
            main_frame,
            text=" 🔑 Generated Password ",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            fg=self.fg_color,
            relief="solid",
            bd=1
        )
        display_frame.pack(fill="x", pady=(0, 15))
        
        # Password text box
        self.password_text = tk.Text(
            display_frame,
            height=3,
            font=("Courier New", 12, "bold"),
            bg="#313244",
            fg=self.success_color,
            wrap="word",
            relief="flat",
            padx=10,
            pady=10
        )
        self.password_text.pack(fill="x", padx=15, pady=15)
        self.password_text.insert("1.0", "Click 'Generate Password' to create a secure password...")
        self.password_text.config(state="disabled")
        
        #  ACTION BUTTONS 
        button_frame = tk.Frame(display_frame, bg=self.bg_color)
        button_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Copy button
        self.copy_btn = tk.Button(
            button_frame,
            text="📋 Copy to Clipboard",
            command=self.copy_to_clipboard,
            font=("Arial", 10, "bold"),
            bg="#313244",
            fg=self.fg_color,
            activebackground=self.accent_color,
            activeforeground=self.bg_color,
            relief="flat",
            cursor="hand2",
            state="disabled"
        )
        self.copy_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        # Clear button
        self.clear_btn = tk.Button(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_password,
            font=("Arial", 10, "bold"),
            bg="#313244",
            fg=self.fg_color,
            activebackground=self.danger_color,
            activeforeground=self.bg_color,
            relief="flat",
            cursor="hand2",
            state="disabled"
        )
        self.clear_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        # STRENGTH INDICATOR 
        self.strength_frame = tk.Frame(main_frame, bg=self.bg_color)
        self.strength_frame.pack(fill="x", pady=(0, 10))
        
        strength_label = tk.Label(
            self.strength_frame,
            text="Password Strength:",
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.fg_color
        )
        strength_label.pack(side="left")
        
        self.strength_indicator = tk.Label(
            self.strength_frame,
            text="Not Generated",
            font=("Arial", 10, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        self.strength_indicator.pack(side="left", padx=10)
        
        
        footer_label = tk.Label(
            main_frame,
            text="💡 Tip: Store your password in a secure password manager",
            font=("Arial", 9, "italic"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        footer_label.pack(pady=(5, 0))
        
    def update_length_label(self, value):
        """Update the length label when slider moves."""
        self.length_label.config(text=str(int(float(value))))
        
    def generate_password(self):
        """
        Generate a secure password based on selected options.
        
        This method validates options, generates the password using
        the secrets module, and updates the display.
        """
        # Check if at least one option is selected
        if not any([
            self.uppercase_var.get(),
            self.lowercase_var.get(),
            self.numbers_var.get(),
            self.special_var.get()
        ]):
            messagebox.showerror(
                "Error",
                "Please select at least ONE character type!"
            )
            return
        
        # Build character pool
        char_pool = ""
        
        if self.uppercase_var.get():
            char_pool += string.ascii_uppercase
        
        if self.lowercase_var.get():
            char_pool += string.ascii_lowercase
        
        if self.numbers_var.get():
            char_pool += string.digits
        
        if self.special_var.get():
            char_pool += string.punctuation
        
        # Generate password using secrets module
        length = self.length_var.get()
        password = ''.join(secrets.choice(char_pool) for _ in range(length))
        
        # Update password display
        self.password_text.config(state="normal")
        self.password_text.delete("1.0", "end")
        self.password_text.insert("1.0", password)
        self.password_text.config(state="disabled")
        
        # Enable buttons
        self.copy_btn.config(state="normal")
        self.clear_btn.config(state="normal")
        
        # Update strength indicator
        self.update_strength_indicator(password)
        
    def update_strength_indicator(self, password):
        """
        Update the password strength indicator.
        
        Args:
            password (str): The generated password
        """
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        
        # Calculate strength score
        score = 0
        if length >= 8:
            score += 1
        if length >= 12:
            score += 1
        if length >= 16:
            score += 1
        if has_upper:
            score += 1
        if has_lower:
            score += 1
        if has_digit:
            score += 1
        if has_special:
            score += 1
        
        # Determine strength level
        if score <= 3:
            strength = "Weak"
            color = self.danger_color
        elif score <= 5:
            strength = "Moderate"
            color = self.warning_color
        else:
            strength = "Strong"
            color = self.success_color
        
        self.strength_indicator.config(text=strength, fg=color)
        
    def copy_to_clipboard(self):
        """Copy the generated password to clipboard."""
        password = self.password_text.get("1.0", "end-1c")
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        messagebox.showinfo(
            "Success",
            "Password copied to clipboard! ✅"
        )
        
    def clear_password(self):
        """Clear the password display."""
        self.password_text.config(state="normal")
        self.password_text.delete("1.0", "end")
        self.password_text.insert("1.0", "Click 'Generate Password' to create a secure password...")
        self.password_text.config(state="disabled")
        
        # Disable buttons
        self.copy_btn.config(state="disabled")
        self.clear_btn.config(state="disabled")
        
        # Reset strength indicator
        self.strength_indicator.config(text="Not Generated", fg=self.fg_color)


def main():
    """
    Main function to run the Password Generator GUI application.
    
    Creates the main window and starts the Tkinter event loop.
    """
    root = tk.Tk()
    app = PasswordGeneratorGUI(root)
    root.mainloop()


# Entry point of the program
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        print("Please report this issue if it persists.")

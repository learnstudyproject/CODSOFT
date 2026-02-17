

import tkinter as tk
from tkinter import messagebox, font
import random


class RockPaperScissorsGUI:
    """Main GUI class for Rock-Paper-Scissors game"""
    
    def __init__(self, root):
        """
        Initialize the GUI application
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("🎮 Rock-Paper-Scissors Game")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        
        # Configure color scheme
        self.bg_color = "#1a1a2e"
        self.secondary_bg = "#16213e"
        self.accent_color = "#0f3460"
        self.highlight_color = "#e94560"
        self.text_color = "#ffffff"
        self.button_hover = "#e94560"
        
        self.root.configure(bg=self.bg_color)
        
        # Initialize game variables
        self.user_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        self.user_choice = None
        self.computer_choice = None
        
        # Choice emojis
        self.emojis = {
            'rock': '🪨',
            'paper': '📄',
            'scissors': '✂️',
            'none': '❓'
        }
        
        # Create GUI components
        self.create_widgets()
        
    def create_widgets(self):
        """Create and arrange all GUI widgets"""
        
        # Title Frame
        title_frame = tk.Frame(self.root, bg=self.bg_color)
        title_frame.pack(pady=20)
        
        title_font = font.Font(family="Arial", size=28, weight="bold")
        title_label = tk.Label(
            title_frame,
            text="🎮 ROCK - PAPER - SCISSORS 🎮",
            font=title_font,
            bg=self.bg_color,
            fg=self.highlight_color
        )
        title_label.pack()
        
        subtitle_font = font.Font(family="Arial", size=12)
        subtitle_label = tk.Label(
            title_frame,
            text="Choose your weapon and defeat the computer!",
            font=subtitle_font,
            bg=self.bg_color,
            fg=self.text_color
        )
        subtitle_label.pack(pady=5)
        
        # Scoreboard Frame
        score_frame = tk.Frame(self.root, bg=self.secondary_bg, relief=tk.RAISED, bd=3)
        score_frame.pack(pady=15, padx=50, fill=tk.X)
        
        score_title_font = font.Font(family="Arial", size=16, weight="bold")
        score_label = tk.Label(
            score_frame,
            text="📊 SCOREBOARD 📊",
            font=score_title_font,
            bg=self.secondary_bg,
            fg=self.highlight_color
        )
        score_label.pack(pady=10)
        
        # Score details
        score_info_frame = tk.Frame(score_frame, bg=self.secondary_bg)
        score_info_frame.pack(pady=5)
        
        score_font = font.Font(family="Arial", size=12, weight="bold")
        
        # User score
        self.user_score_label = tk.Label(
            score_info_frame,
            text=f"👤 You: {self.user_score}",
            font=score_font,
            bg=self.secondary_bg,
            fg="#4ecca3",
            width=15
        )
        self.user_score_label.grid(row=0, column=0, padx=20)
        
        # Rounds
        self.rounds_label = tk.Label(
            score_info_frame,
            text=f"🎯 Rounds: {self.rounds_played}",
            font=score_font,
            bg=self.secondary_bg,
            fg="#f5f5f5",
            width=15
        )
        self.rounds_label.grid(row=0, column=1, padx=20)
        
        # Computer score
        self.computer_score_label = tk.Label(
            score_info_frame,
            text=f"🤖 Computer: {self.computer_score}",
            font=score_font,
            bg=self.secondary_bg,
            fg="#ff6b6b",
            width=15
        )
        self.computer_score_label.grid(row=0, column=2, padx=20)
        
        # Choices Display Frame
        choices_frame = tk.Frame(self.root, bg=self.bg_color)
        choices_frame.pack(pady=20)
        
        choice_font = font.Font(family="Arial", size=48)
        label_font = font.Font(family="Arial", size=12, weight="bold")
        
        # User choice display
        user_choice_frame = tk.Frame(choices_frame, bg=self.accent_color, relief=tk.RAISED, bd=3)
        user_choice_frame.grid(row=0, column=0, padx=30)
        
        tk.Label(
            user_choice_frame,
            text="Your Choice",
            font=label_font,
            bg=self.accent_color,
            fg=self.text_color
        ).pack(pady=5)
        
        self.user_choice_label = tk.Label(
            user_choice_frame,
            text=self.emojis['none'],
            font=choice_font,
            bg=self.accent_color,
            fg=self.text_color,
            width=4,
            height=2
        )
        self.user_choice_label.pack(pady=10)
        
        # VS Label
        vs_font = font.Font(family="Arial", size=24, weight="bold")
        tk.Label(
            choices_frame,
            text="VS",
            font=vs_font,
            bg=self.bg_color,
            fg=self.highlight_color
        ).grid(row=0, column=1, padx=20)
        
        # Computer choice display
        computer_choice_frame = tk.Frame(choices_frame, bg=self.accent_color, relief=tk.RAISED, bd=3)
        computer_choice_frame.grid(row=0, column=2, padx=30)
        
        tk.Label(
            computer_choice_frame,
            text="Computer Choice",
            font=label_font,
            bg=self.accent_color,
            fg=self.text_color
        ).pack(pady=5)
        
        self.computer_choice_label = tk.Label(
            computer_choice_frame,
            text=self.emojis['none'],
            font=choice_font,
            bg=self.accent_color,
            fg=self.text_color,
            width=4,
            height=2
        )
        self.computer_choice_label.pack(pady=10)
        
        # Result Label
        result_font = font.Font(family="Arial", size=18, weight="bold")
        self.result_label = tk.Label(
            self.root,
            text="Make your choice to start!",
            font=result_font,
            bg=self.bg_color,
            fg=self.text_color,
            pady=15
        )
        self.result_label.pack()
        
        # Buttons Frame
        buttons_frame = tk.Frame(self.root, bg=self.bg_color)
        buttons_frame.pack(pady=20)
        
        button_font = font.Font(family="Arial", size=14, weight="bold")
        
        # Create choice buttons
        self.rock_button = self.create_choice_button(
            buttons_frame, "ROCK 🪨", "rock", button_font, 0
        )
        self.paper_button = self.create_choice_button(
            buttons_frame, "PAPER 📄", "paper", button_font, 1
        )
        self.scissors_button = self.create_choice_button(
            buttons_frame, "SCISSORS ✂️", "scissors", button_font, 2
        )
        
        # Control buttons frame
        control_frame = tk.Frame(self.root, bg=self.bg_color)
        control_frame.pack(pady=15)
        
        control_font = font.Font(family="Arial", size=11, weight="bold")
        
        # Reset button
        reset_button = tk.Button(
            control_frame,
            text="🔄 Reset Scores",
            font=control_font,
            bg=self.accent_color,
            fg=self.text_color,
            activebackground=self.button_hover,
            activeforeground=self.text_color,
            cursor="hand2",
            width=15,
            height=2,
            relief=tk.RAISED,
            bd=3,
            command=self.reset_game
        )
        reset_button.grid(row=0, column=0, padx=10)
        
        # Rules button
        rules_button = tk.Button(
            control_frame,
            text="📖 View Rules",
            font=control_font,
            bg=self.accent_color,
            fg=self.text_color,
            activebackground=self.button_hover,
            activeforeground=self.text_color,
            cursor="hand2",
            width=15,
            height=2,
            relief=tk.RAISED,
            bd=3,
            command=self.show_rules
        )
        rules_button.grid(row=0, column=1, padx=10)
        
        # Exit button
        exit_button = tk.Button(
            control_frame,
            text="🚪 Exit Game",
            font=control_font,
            bg=self.highlight_color,
            fg=self.text_color,
            activebackground="#c23e57",
            activeforeground=self.text_color,
            cursor="hand2",
            width=15,
            height=2,
            relief=tk.RAISED,
            bd=3,
            command=self.exit_game
        )
        exit_button.grid(row=0, column=2, padx=10)
        
    def create_choice_button(self, parent, text, choice, font_obj, column):
        """
        Create a styled choice button
        Args:
            parent: Parent widget
            text: Button text
            choice: Choice value (rock/paper/scissors)
            font_obj: Font object
            column: Grid column position
        Returns: Button widget
        """
        button = tk.Button(
            parent,
            text=text,
            font=font_obj,
            bg=self.accent_color,
            fg=self.text_color,
            activebackground=self.button_hover,
            activeforeground=self.text_color,
            cursor="hand2",
            width=15,
            height=3,
            relief=tk.RAISED,
            bd=5,
            command=lambda: self.play_round(choice)
        )
        button.grid(row=0, column=column, padx=15)
        
        # Add hover effects
        button.bind("<Enter>", lambda e: self.on_button_hover(button, True))
        button.bind("<Leave>", lambda e: self.on_button_hover(button, False))
        
        return button
    
    def on_button_hover(self, button, is_entering):
        """
        Handle button hover effect
        Args:
            button: Button widget
            is_entering: True if mouse entering, False if leaving
        """
        if is_entering:
            button.config(bg=self.button_hover)
        else:
            button.config(bg=self.accent_color)
    
    def play_round(self, user_choice):
        """
        Play one round of the game
        Args:
            user_choice: User's choice (rock/paper/scissors)
        """
        # Store user choice
        self.user_choice = user_choice
        
        # Generate computer choice
        self.computer_choice = random.choice(['rock', 'paper', 'scissors'])
        
        # Update choice displays
        self.user_choice_label.config(text=self.emojis[self.user_choice])
        self.computer_choice_label.config(text=self.emojis[self.computer_choice])
        
        # Determine winner
        result = self.determine_winner(self.user_choice, self.computer_choice)
        
        # Update scores
        self.rounds_played += 1
        if result == "win":
            self.user_score += 1
        elif result == "lose":
            self.computer_score += 1
        
        # Update displays
        self.update_score_display()
        self.display_result(result)
        
    def determine_winner(self, user_choice, computer_choice):
        """
        Determine the winner
        Args:
            user_choice: User's choice
            computer_choice: Computer's choice
        Returns: 'win', 'lose', or 'tie'
        """
        if user_choice == computer_choice:
            return "tie"
        
        if (user_choice == 'rock' and computer_choice == 'scissors') or \
           (user_choice == 'scissors' and computer_choice == 'paper') or \
           (user_choice == 'paper' and computer_choice == 'rock'):
            return "win"
        
        return "lose"
    
    def display_result(self, result):
        """
        Display the round result
        Args:
            result: 'win', 'lose', or 'tie'
        """
        if result == "tie":
            self.result_label.config(
                text="🤝 IT'S A TIE! 🤝",
                fg="#ffd700"
            )
        elif result == "win":
            reason = self.get_win_reason(self.user_choice, self.computer_choice)
            self.result_label.config(
                text=f"🎉 YOU WIN! 🎉\n{reason}",
                fg="#4ecca3"
            )
        else:
            reason = self.get_win_reason(self.computer_choice, self.user_choice)
            self.result_label.config(
                text=f"😢 YOU LOSE! 😢\n{reason}",
                fg="#ff6b6b"
            )
    
    def get_win_reason(self, winner_choice, loser_choice):
        """
        Get the reason for winning
        Args:
            winner_choice: Winning choice
            loser_choice: Losing choice
        Returns: Reason string
        """
        reasons = {
            ('rock', 'scissors'): 'Rock crushes Scissors!',
            ('scissors', 'paper'): 'Scissors cut Paper!',
            ('paper', 'rock'): 'Paper covers Rock!'
        }
        return reasons.get((winner_choice, loser_choice), '')
    
    def update_score_display(self):
        """Update the scoreboard display"""
        self.user_score_label.config(text=f"👤 You: {self.user_score}")
        self.computer_score_label.config(text=f"🤖 Computer: {self.computer_score}")
        self.rounds_label.config(text=f"🎯 Rounds: {self.rounds_played}")
    
    def reset_game(self):
        """Reset the game scores and choices"""
        response = messagebox.askyesno(
            "Reset Game",
            "Are you sure you want to reset all scores?"
        )
        
        if response:
            self.user_score = 0
            self.computer_score = 0
            self.rounds_played = 0
            
            self.update_score_display()
            self.user_choice_label.config(text=self.emojis['none'])
            self.computer_choice_label.config(text=self.emojis['none'])
            self.result_label.config(
                text="Scores reset! Make your choice to start!",
                fg=self.text_color
            )
    
    def show_rules(self):
        """Display the game rules in a message box"""
        rules_text = """
🎮 ROCK-PAPER-SCISSORS RULES 🎮

📖 How to Play:
1. Choose Rock, Paper, or Scissors
2. Computer makes its choice
3. Winner is determined by:
   
   🪨 Rock beats Scissors
      (Rock crushes Scissors)
   
   ✂️ Scissors beat Paper
      (Scissors cut Paper)
   
   📄 Paper beats Rock
      (Paper covers Rock)

4. First to get the most points wins!

🏆 Scoring:
• Win = 1 point
• Lose = 0 points
• Tie = No points

Good luck and have fun! 🎉
        """
        messagebox.showinfo("Game Rules", rules_text)
    
    def exit_game(self):
        """Exit the game with confirmation"""
        if self.rounds_played > 0:
            # Show final stats
            ties = self.rounds_played - self.user_score - self.computer_score
            win_rate = (self.user_score / self.rounds_played) * 100 if self.rounds_played > 0 else 0
            
            if self.user_score > self.computer_score:
                final_msg = f"🎊 CONGRATULATIONS! YOU WON! 🎊\n\n"
            elif self.computer_score > self.user_score:
                final_msg = f"💻 Computer won this time! 💻\n\n"
            else:
                final_msg = f"🤝 It's a perfect tie! 🤝\n\n"
            
            final_msg += f"Final Statistics:\n"
            final_msg += f"Rounds Played: {self.rounds_played}\n"
            final_msg += f"Your Score: {self.user_score}\n"
            final_msg += f"Computer Score: {self.computer_score}\n"
            final_msg += f"Ties: {ties}\n"
            final_msg += f"Your Win Rate: {win_rate:.1f}%\n\n"
            final_msg += f"Thanks for playing!"
            
            messagebox.showinfo("Game Over", final_msg)
        
        self.root.quit()


def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = RockPaperScissorsGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()



import random
import os
import sys


def clear_screen():
    """Clear the console screen for better user experience"""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_banner():
    """Display the game banner/logo"""
    banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║        🪨  ROCK - PAPER - SCISSORS GAME  ✂️           ║
    ║                                                       ║
    ║              Let's Play and Have Fun! 🎮             ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """
    print(banner)


def display_rules():
    """Display the game rules to the player"""
    print("\n" + "="*60)
    print("                      GAME RULES")
    print("="*60)
    print("  🪨  Rock beats Scissors     (Rock crushes Scissors)")
    print("  ✂️  Scissors beat Paper      (Scissors cut Paper)")
    print("  📄  Paper beats Rock        (Paper covers Rock)")
    print("="*60 + "\n")


def get_user_choice():
    """
    Get and validate user's choice
    Returns: string (rock, paper, or scissors)
    """
    choices = ['rock', 'paper', 'scissors']
    
    while True:
        print("\n📝 Make your choice:")
        print("  1. Rock 🪨")
        print("  2. Paper 📄")
        print("  3. Scissors ✂️")
        print("  4. View Rules")
        print("  5. Exit Game")
        
        user_input = input("\n👉 Enter your choice (1-5 or rock/paper/scissors): ").strip().lower()
        
        # Handle numeric input
        if user_input == '1' or user_input == 'rock':
            return 'rock'
        elif user_input == '2' or user_input == 'paper':
            return 'paper'
        elif user_input == '3' or user_input == 'scissors':
            return 'scissors'
        elif user_input == '4':
            display_rules()
            continue
        elif user_input == '5':
            print("\n👋 Thanks for playing! Goodbye!\n")
            sys.exit(0)
        else:
            print("\n❌ Invalid input! Please choose 1-5 or type rock/paper/scissors.")


def get_computer_choice():
    """
    Generate random choice for computer
    Returns: string (rock, paper, or scissors)
    """
    choices = ['rock', 'paper', 'scissors']
    return random.choice(choices)


def get_emoji(choice):
    """
    Get emoji representation for a choice
    Args: choice (string)
    Returns: emoji string
    """
    emojis = {
        'rock': '🪨',
        'paper': '📄',
        'scissors': '✂️'
    }
    return emojis.get(choice, '')


def determine_winner(user_choice, computer_choice):
    """
    Determine the winner based on game logic
    Args:
        user_choice (string): User's choice
        computer_choice (string): Computer's choice
    Returns: 
        tuple: (result_string, points_for_user, points_for_computer)
    """
    # Tie condition
    if user_choice == computer_choice:
        return ("tie", 0, 0)
    
    # User wins conditions
    if (user_choice == 'rock' and computer_choice == 'scissors') or \
       (user_choice == 'scissors' and computer_choice == 'paper') or \
       (user_choice == 'paper' and computer_choice == 'rock'):
        return ("win", 1, 0)
    
    # Computer wins (all other cases)
    return ("lose", 0, 1)


def display_choices(user_choice, computer_choice):
    """Display both player's and computer's choices"""
    print("\n" + "="*60)
    print("                    CHOICES MADE")
    print("="*60)
    print(f"  👤 You chose:        {user_choice.capitalize()} {get_emoji(user_choice)}")
    print(f"  🤖 Computer chose:   {computer_choice.capitalize()} {get_emoji(computer_choice)}")
    print("="*60)


def display_result(result, user_choice, computer_choice):
    """
    Display the game result with animation
    Args:
        result (string): win, lose, or tie
        user_choice (string): User's choice
        computer_choice (string): Computer's choice
    """
    print("\n" + "🎯 " + "="*56 + " 🎯")
    
    if result == "tie":
        print("                    🤝 IT'S A TIE! 🤝")
        print("              Both players chose the same!")
    elif result == "win":
        print("                   🎉 YOU WIN! 🎉")
        reason = get_win_reason(user_choice, computer_choice)
        print(f"              {reason}")
    else:
        print("                   😢 YOU LOSE! 😢")
        reason = get_win_reason(computer_choice, user_choice)
        print(f"              {reason}")
    
    print("🎯 " + "="*56 + " 🎯\n")


def get_win_reason(winner_choice, loser_choice):
    """
    Get the reason why a choice won
    Args:
        winner_choice (string): Winning choice
        loser_choice (string): Losing choice
    Returns: string explaining why
    """
    reasons = {
        ('rock', 'scissors'): 'Rock crushes Scissors!',
        ('scissors', 'paper'): 'Scissors cut Paper!',
        ('paper', 'rock'): 'Paper covers Rock!'
    }
    return reasons.get((winner_choice, loser_choice), '')


def display_score(user_score, computer_score, rounds_played):
    """
    Display the current score
    Args:
        user_score (int): User's score
        computer_score (int): Computer's score
        rounds_played (int): Total rounds played
    """
    print("\n" + "📊 " + "="*54 + " 📊")
    print("                      SCOREBOARD")
    print("="*60)
    print(f"  Rounds Played: {rounds_played}")
    print(f"  👤 Your Score:     {user_score}")
    print(f"  🤖 Computer Score: {computer_score}")
    
    if user_score > computer_score:
        print("\n  🏆 You're in the lead! Keep it up!")
    elif computer_score > user_score:
        print("\n  💪 Computer is ahead! You can catch up!")
    else:
        print("\n  ⚖️  It's a perfect tie!")
    
    print("📊 " + "="*54 + " 📊\n")


def play_again():
    """
    Ask if user wants to play another round
    Returns: boolean
    """
    while True:
        choice = input("\n🔄 Do you want to play again? (yes/no): ").strip().lower()
        if choice in ['yes', 'y', '1']:
            return True
        elif choice in ['no', 'n', '0']:
            return False
        else:
            print("❌ Please enter 'yes' or 'no'.")


def display_final_stats(user_score, computer_score, rounds_played):
    """
    Display final game statistics
    Args:
        user_score (int): User's total score
        computer_score (int): Computer's total score
        rounds_played (int): Total rounds played
    """
    clear_screen()
    print("\n" + "🏁 " + "="*54 + " 🏁")
    print("                   FINAL STATISTICS")
    print("="*60)
    print(f"  Total Rounds Played: {rounds_played}")
    print(f"  👤 Your Score:        {user_score}")
    print(f"  🤖 Computer Score:    {computer_score}")
    
    ties = rounds_played - user_score - computer_score
    print(f"  🤝 Ties:              {ties}")
    
    if rounds_played > 0:
        win_rate = (user_score / rounds_played) * 100
        print(f"\n  📈 Your Win Rate:     {win_rate:.1f}%")
    
    print("\n" + "-"*60)
    
    # Determine overall winner
    if user_score > computer_score:
        print("\n      🎊🎉 CONGRATULATIONS! YOU ARE THE CHAMPION! 🎉🎊")
    elif computer_score > user_score:
        print("\n         💻 Computer wins this time! Better luck next time!")
    else:
        print("\n              🤝 It's a perfect tie overall! 🤝")
    
    print("\n" + "🏁 " + "="*54 + " 🏁\n")
    print("\n        Thank you for playing Rock-Paper-Scissors! 🎮\n")


def main():
    """Main game loop"""
    # Initialize scores
    user_score = 0
    computer_score = 0
    rounds_played = 0
    
    # Display welcome screen
    clear_screen()
    display_banner()
    
    print("\n👋 Welcome to Rock-Paper-Scissors Game!")
    print("   Get ready for an exciting challenge!\n")
    
    # Ask if user wants to see rules
    show_rules = input("📖 Do you want to see the rules? (yes/no): ").strip().lower()
    if show_rules in ['yes', 'y', '1']:
        display_rules()
    
    input("\n✅ Press Enter to start the game...")
    
    # Main game loop
    while True:
        clear_screen()
        display_banner()
        
        # Display current score
        if rounds_played > 0:
            display_score(user_score, computer_score, rounds_played)
        
        # Get choices
        user_choice = get_user_choice()
        computer_choice = get_computer_choice()
        
        # Display choices
        display_choices(user_choice, computer_choice)
        
        # Determine winner
        result, user_points, computer_points = determine_winner(user_choice, computer_choice)
        
        # Update scores
        user_score += user_points
        computer_score += computer_points
        rounds_played += 1
        
        # Display result
        display_result(result, user_choice, computer_choice)
        
        # Display updated score
        display_score(user_score, computer_score, rounds_played)
        
        # Ask to play again
        if not play_again():
            break
    
    # Display final statistics
    display_final_stats(user_score, computer_score, rounds_played)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Game interrupted by user. Goodbye! 👋\n")
        sys.exit(0)

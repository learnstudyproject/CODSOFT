"""
To-Do List Application - Command Line Interface Version
This module provides a clean menu-based CLI for managing tasks.

Author: Professional Python Developer
Date: 2026-02-17
"""

import sys
from todo_core import TodoManager


class TodoCLI:
    """
    Command Line Interface for the To-Do List application.
    Provides a menu-based interface for all task operations.
    """
    
    def __init__(self):
        """Initialize the CLI with a TodoManager instance."""
        print("=" * 60)
        print(" " * 15 + "TO-DO LIST APPLICATION")
        print(" " * 15 + "Command Line Interface")
        print("=" * 60)
        print()
        
        self.manager = TodoManager()
        self.running = True
    
    def clear_screen(self):
        """Clear the console screen (works on both Windows and Unix)."""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_menu(self):
        """Display the main menu options."""
        print("\n" + "=" * 60)
        print(" " * 20 + "MAIN MENU")
        print("=" * 60)
        print("  1. Add New Task")
        print("  2. View All Tasks")
        print("  3. View Pending Tasks")
        print("  4. View Completed Tasks")
        print("  5. Update Task")
        print("  6. Mark Task as Completed")
        print("  7. Mark Task as Pending")
        print("  8. Delete Task")
        print("  9. Delete All Completed Tasks")
        print(" 10. Task Statistics")
        print("  0. Exit")
        print("=" * 60)
    
    def get_input(self, prompt: str, input_type=str, allow_empty=False):
        """
        Get and validate user input.
        
        Args:
            prompt (str): Prompt to display
            input_type (type): Expected input type (str, int, etc.)
            allow_empty (bool): Whether to allow empty input
            
        Returns:
            Validated input of the specified type, or None if invalid
        """
        while True:
            try:
                user_input = input(prompt).strip()
                
                if not user_input and not allow_empty:
                    print("✗ Input cannot be empty! Please try again.")
                    continue
                
                if user_input == "" and allow_empty:
                    return None
                
                if input_type == int:
                    return int(user_input)
                elif input_type == str:
                    return user_input
                else:
                    return input_type(user_input)
                    
            except ValueError:
                print(f"✗ Invalid input! Expected {input_type.__name__}. Please try again.")
            except KeyboardInterrupt:
                print("\n✗ Input cancelled.")
                return None
    
    def display_tasks(self, tasks, title="All Tasks"):
        """
        Display a list of tasks in a formatted table.
        
        Args:
            tasks (list): List of Task objects to display
            title (str): Title for the task list
        """
        print("\n" + "-" * 60)
        print(f" {title}")
        print("-" * 60)
        
        if not tasks:
            print("  No tasks to display.")
        else:
            print(f"{'ID':<5} {'Status':<10} {'Task Title':<30} {'Updated':<15}")
            print("-" * 60)
            for task in tasks:
                status = "✓ Done" if task.completed else "✗ Pending"
                title_truncated = task.title[:27] + "..." if len(task.title) > 30 else task.title
                updated = task.updated_at.split()[0]  # Just the date
                print(f"{task.id:<5} {status:<10} {title_truncated:<30} {updated:<15}")
        
        print("-" * 60)
    
    def add_task(self):
        """Handle adding a new task."""
        print("\n" + "=" * 60)
        print(" ADD NEW TASK")
        print("=" * 60)
        
        title = self.get_input("Enter task title (or press Enter to cancel): ", str, allow_empty=True)
        
        if title:
            self.manager.add_task(title)
        else:
            print("ℹ Task creation cancelled.")
    
    def view_all_tasks(self):
        """Display all tasks."""
        tasks = self.manager.get_all_tasks()
        self.display_tasks(tasks, "All Tasks")
    
    def view_pending_tasks(self):
        """Display only pending tasks."""
        all_tasks = self.manager.get_all_tasks()
        pending_tasks = [task for task in all_tasks if not task.completed]
        self.display_tasks(pending_tasks, "Pending Tasks")
    
    def view_completed_tasks(self):
        """Display only completed tasks."""
        all_tasks = self.manager.get_all_tasks()
        completed_tasks = [task for task in all_tasks if task.completed]
        self.display_tasks(completed_tasks, "Completed Tasks")
    
    def update_task(self):
        """Handle updating an existing task."""
        print("\n" + "=" * 60)
        print(" UPDATE TASK")
        print("=" * 60)
        
        # Show all tasks first
        self.view_all_tasks()
        
        task_id = self.get_input("\nEnter task ID to update (or 0 to cancel): ", int, allow_empty=True)
        
        if task_id is None or task_id == 0:
            print("ℹ Update cancelled.")
            return
        
        task = self.manager.get_task_by_id(task_id)
        if not task:
            print(f"✗ Task with ID {task_id} not found!")
            return
        
        print(f"\nCurrent title: {task.title}")
        new_title = self.get_input("Enter new title (or press Enter to cancel): ", str, allow_empty=True)
        
        if new_title:
            self.manager.update_task(task_id, new_title)
        else:
            print("ℹ Update cancelled.")
    
    def mark_completed(self):
        """Mark a task as completed."""
        print("\n" + "=" * 60)
        print(" MARK TASK AS COMPLETED")
        print("=" * 60)
        
        # Show pending tasks
        self.view_pending_tasks()
        
        task_id = self.get_input("\nEnter task ID to mark as completed (or 0 to cancel): ", int, allow_empty=True)
        
        if task_id is None or task_id == 0:
            print("ℹ Operation cancelled.")
            return
        
        self.manager.set_task_status(task_id, completed=True)
    
    def mark_pending(self):
        """Mark a task as pending."""
        print("\n" + "=" * 60)
        print(" MARK TASK AS PENDING")
        print("=" * 60)
        
        # Show completed tasks
        self.view_completed_tasks()
        
        task_id = self.get_input("\nEnter task ID to mark as pending (or 0 to cancel): ", int, allow_empty=True)
        
        if task_id is None or task_id == 0:
            print("ℹ Operation cancelled.")
            return
        
        self.manager.set_task_status(task_id, completed=False)
    
    def delete_task(self):
        """Handle deleting a task."""
        print("\n" + "=" * 60)
        print(" DELETE TASK")
        print("=" * 60)
        
        # Show all tasks
        self.view_all_tasks()
        
        task_id = self.get_input("\nEnter task ID to delete (or 0 to cancel): ", int, allow_empty=True)
        
        if task_id is None or task_id == 0:
            print("ℹ Deletion cancelled.")
            return
        
        task = self.manager.get_task_by_id(task_id)
        if not task:
            print(f"✗ Task with ID {task_id} not found!")
            return
        
        print(f"\nTask to delete: {task.title}")
        confirm = self.get_input("Are you sure? (yes/no): ", str)
        
        if confirm.lower() in ['yes', 'y']:
            self.manager.delete_task(task_id)
        else:
            print("ℹ Deletion cancelled.")
    
    def delete_completed_tasks(self):
        """Delete all completed tasks."""
        print("\n" + "=" * 60)
        print(" DELETE ALL COMPLETED TASKS")
        print("=" * 60)
        
        # Show completed tasks
        self.view_completed_tasks()
        
        completed_count = self.manager.get_task_count()['completed']
        
        if completed_count == 0:
            return
        
        confirm = self.get_input(f"\nDelete {completed_count} completed task(s)? (yes/no): ", str)
        
        if confirm.lower() in ['yes', 'y']:
            self.manager.clear_completed_tasks()
        else:
            print("ℹ Deletion cancelled.")
    
    def show_statistics(self):
        """Display task statistics."""
        print("\n" + "=" * 60)
        print(" TASK STATISTICS")
        print("=" * 60)
        
        stats = self.manager.get_task_count()
        
        print(f"\n  Total Tasks:      {stats['total']}")
        print(f"  Completed Tasks:  {stats['completed']}")
        print(f"  Pending Tasks:    {stats['pending']}")
        
        if stats['total'] > 0:
            completion_rate = (stats['completed'] / stats['total']) * 100
            print(f"  Completion Rate:  {completion_rate:.1f}%")
            
            # Progress bar
            bar_length = 30
            filled = int(bar_length * stats['completed'] / stats['total'])
            bar = '█' * filled + '░' * (bar_length - filled)
            print(f"\n  Progress: [{bar}] {completion_rate:.1f}%")
        
        print("=" * 60)
    
    def run(self):
        """Main application loop."""
        while self.running:
            try:
                self.display_menu()
                
                choice = self.get_input("\nEnter your choice (0-10): ", int, allow_empty=True)
                
                if choice is None:
                    continue
                
                if choice == 1:
                    self.add_task()
                elif choice == 2:
                    self.view_all_tasks()
                elif choice == 3:
                    self.view_pending_tasks()
                elif choice == 4:
                    self.view_completed_tasks()
                elif choice == 5:
                    self.update_task()
                elif choice == 6:
                    self.mark_completed()
                elif choice == 7:
                    self.mark_pending()
                elif choice == 8:
                    self.delete_task()
                elif choice == 9:
                    self.delete_completed_tasks()
                elif choice == 10:
                    self.show_statistics()
                elif choice == 0:
                    self.exit_application()
                else:
                    print("✗ Invalid choice! Please enter a number between 0 and 10.")
                
                # Pause before showing menu again
                if self.running and choice != 0:
                    input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n✗ Interrupted by user.")
                self.exit_application()
            except Exception as e:
                print(f"\n✗ An unexpected error occurred: {e}")
                print("Please try again.")
    
    def exit_application(self):
        """Exit the application gracefully."""
        print("\n" + "=" * 60)
        print(" " * 15 + "Thank you for using")
        print(" " * 15 + "TO-DO LIST APPLICATION!")
        print("=" * 60)
        print()
        self.running = False


def main():
    """Entry point for the CLI application."""
    try:
        app = TodoCLI()
        app.run()
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

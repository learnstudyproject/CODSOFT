

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class Task:
    """
    Represents a single task in the to-do list.
    
    Attributes:
        id (int): Unique identifier for the task
        title (str): Task title/description
        completed (bool): Task completion status
        created_at (str): Timestamp when task was created
        updated_at (str): Timestamp when task was last updated
    """
    
    def __init__(self, id: int, title: str, completed: bool = False, 
                 created_at: str = None, updated_at: str = None):
        """Initialize a new task."""
        self.id = id
        self.title = title
        self.completed = completed
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = updated_at or self.created_at
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """Create a task from dictionary."""
        return cls(
            id=data['id'],
            title=data['title'],
            completed=data.get('completed', False),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def __str__(self) -> str:
        """String representation of the task."""
        status = "✓" if self.completed else "✗"
        return f"[{status}] {self.id}. {self.title}"


class TodoManager:
    """
    Manages all task operations including CRUD operations and persistence.
    
    This class handles:
    - Adding new tasks
    - Viewing all tasks
    - Updating existing tasks
    - Marking tasks as completed/pending
    - Deleting tasks
    - Saving and loading tasks from JSON file
    """
    
    def __init__(self, data_file: str = "tasks.json"):
        """
        Initialize the TodoManager.
        
        Args:
            data_file (str): Path to the JSON file for storing tasks
        """
        self.data_file = data_file
        self.tasks: List[Task] = []
        self.load_tasks()
    
    def load_tasks(self) -> None:
        """Load tasks from JSON file. Creates empty file if it doesn't exist."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in data]
                print(f"✓ Loaded {len(self.tasks)} tasks from {self.data_file}")
            else:
                self.tasks = []
                self.save_tasks()  # Create empty file
                print(f"✓ Created new task file: {self.data_file}")
        except json.JSONDecodeError:
            print(f"⚠ Warning: Could not parse {self.data_file}. Starting with empty task list.")
            self.tasks = []
        except Exception as e:
            print(f"⚠ Error loading tasks: {e}")
            self.tasks = []
    
    def save_tasks(self) -> bool:
        """
        Save all tasks to JSON file.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([task.to_dict() for task in self.tasks], f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"✗ Error saving tasks: {e}")
            return False
    
    def get_next_id(self) -> int:
        """Get the next available task ID."""
        if not self.tasks:
            return 1
        return max(task.id for task in self.tasks) + 1
    
    def add_task(self, title: str) -> Optional[Task]:
        """
        Add a new task.
        
        Args:
            title (str): Task title/description
            
        Returns:
            Task: The created task, or None if failed
        """
        if not title or not title.strip():
            print("✗ Error: Task title cannot be empty!")
            return None
        
        task = Task(id=self.get_next_id(), title=title.strip())
        self.tasks.append(task)
        
        if self.save_tasks():
            print(f"✓ Task added successfully! (ID: {task.id})")
            return task
        else:
            self.tasks.pop()  # Remove from list if save failed
            return None
    
    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks.
        
        Returns:
            List[Task]: List of all tasks
        """
        return self.tasks.copy()
    
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Find a task by ID.
        
        Args:
            task_id (int): Task ID to search for
            
        Returns:
            Task: The task if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def update_task(self, task_id: int, new_title: str) -> bool:
        """
        Update a task's title.
        
        Args:
            task_id (int): ID of task to update
            new_title (str): New title for the task
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not new_title or not new_title.strip():
            print("✗ Error: Task title cannot be empty!")
            return False
        
        task = self.get_task_by_id(task_id)
        if not task:
            print(f"✗ Error: Task with ID {task_id} not found!")
            return False
        
        old_title = task.title
        task.title = new_title.strip()
        task.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if self.save_tasks():
            print(f"✓ Task updated successfully!")
            print(f"  Old: {old_title}")
            print(f"  New: {task.title}")
            return True
        else:
            task.title = old_title  # Revert on save failure
            return False
    
    def toggle_task_status(self, task_id: int) -> bool:
        """
        Toggle a task's completion status.
        
        Args:
            task_id (int): ID of task to toggle
            
        Returns:
            bool: True if successful, False otherwise
        """
        task = self.get_task_by_id(task_id)
        if not task:
            print(f"✗ Error: Task with ID {task_id} not found!")
            return False
        
        task.completed = not task.completed
        task.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if self.save_tasks():
            status = "completed" if task.completed else "pending"
            print(f"✓ Task marked as {status}!")
            return True
        else:
            task.completed = not task.completed  # Revert on save failure
            return False
    
    def set_task_status(self, task_id: int, completed: bool) -> bool:
        """
        Set a task's completion status.
        
        Args:
            task_id (int): ID of task to update
            completed (bool): New completion status
            
        Returns:
            bool: True if successful, False otherwise
        """
        task = self.get_task_by_id(task_id)
        if not task:
            print(f"✗ Error: Task with ID {task_id} not found!")
            return False
        
        if task.completed == completed:
            status = "completed" if completed else "pending"
            print(f"ℹ Task is already {status}!")
            return True
        
        task.completed = completed
        task.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if self.save_tasks():
            status = "completed" if completed else "pending"
            print(f"✓ Task marked as {status}!")
            return True
        else:
            task.completed = not completed  # Revert on save failure
            return False
    
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task.
        
        Args:
            task_id (int): ID of task to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        task = self.get_task_by_id(task_id)
        if not task:
            print(f"✗ Error: Task with ID {task_id} not found!")
            return False
        
        self.tasks.remove(task)
        
        if self.save_tasks():
            print(f"✓ Task deleted successfully!")
            return True
        else:
            self.tasks.append(task)  # Restore on save failure
            return False
    
    def get_task_count(self) -> Dict[str, int]:
        """
        Get task statistics.
        
        Returns:
            dict: Dictionary with total, completed, and pending counts
        """
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task.completed)
        pending = total - completed
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending
        }
    
    def clear_completed_tasks(self) -> int:
        """
        Remove all completed tasks.
        
        Returns:
            int: Number of tasks deleted
        """
        initial_count = len(self.tasks)
        self.tasks = [task for task in self.tasks if not task.completed]
        deleted_count = initial_count - len(self.tasks)
        
        if deleted_count > 0:
            self.save_tasks()
            print(f"✓ Deleted {deleted_count} completed task(s)!")
        else:
            print("ℹ No completed tasks to delete!")
        
        return deleted_count


# Example usage and testing
if __name__ == "__main__":
    print("=" * 50)
    print("TODO CORE MODULE - Testing")
    print("=" * 50)
    
    # Create a manager instance
    manager = TodoManager("test_tasks.json")
    
    # Add some tasks
    print("\n--- Adding Tasks ---")
    manager.add_task("Complete Python project")
    manager.add_task("Study for exam")
    manager.add_task("Buy groceries")
    
    # View all tasks
    print("\n--- All Tasks ---")
    for task in manager.get_all_tasks():
        print(task)
    
    # Mark a task as completed
    print("\n--- Marking Task as Completed ---")
    manager.toggle_task_status(1)
    
    # Update a task
    print("\n--- Updating Task ---")
    manager.update_task(2, "Study for Python exam")
    
    # Show statistics
    print("\n--- Task Statistics ---")
    stats = manager.get_task_count()
    print(f"Total: {stats['total']}")
    print(f"Completed: {stats['completed']}")
    print(f"Pending: {stats['pending']}")
    
    print("\n" + "=" * 50)

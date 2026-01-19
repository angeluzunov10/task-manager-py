from models import PersonalTask, WorkTask
from task_manager import TaskManager
from database import engine, Base
import models

Base.metadata.create_all(bind=engine) # Този ред създава таблиците в базата данни, ако те не съществуват

def main():
    manager = TaskManager()
    # manager.load_from_file("tasks.json")

    while True:
        print("\n--- Task Manager Menu ---")
        print("1. Add Work Task")
        print("2. Add Personal Task")
        print("3. List All Tasks")
        print("4. Mark Task as Completed by ID")
        print("5. Delete Task by ID")
        print("6. Save and Exit")

        choice = input("Select an option (1-6): ")

        if choice == "1":
            # Тук събери вход за WorkTask
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            deadline = input("Enter task deadline (YYYY-MM-DD): ")

            task = WorkTask(title=title, description=description, deadline=deadline, type='WorkTask')
            manager.add_task(task)
            print(f"Work task '{title}' added.")

        elif choice == "2":
            # Тук събери вход за PersonalTask
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            priority = input("Enter task priority (Low/Medium/High): ")
            task = PersonalTask(title=title, description=description, priority=priority, type='PersonalTask')
            manager.add_task(task)
            print(f"Personal task '{title}' added.")

        elif choice == "3":
            manager.list_tasks()

        elif choice == "4":
            try:
                task_id = int(input("Enter the ID of the task to complete: "))
                task = manager.get_task_by_id(task_id)
                if task:
                    task.complete_task()
                    # Важно: Когато променим атрибут на обект, трябва да комитнем сесията
                    manager.db.commit() 
                    print(f"Task ID {task_id} marked as completed.")
                else:
                    print(f"Task with ID {task_id} not found.")
            except ValueError:
                print("Please enter a valid number for ID.")

        elif choice == "5":
            try:
                task_id = int(input("Enter the ID of the task to delete: "))
                manager.delete_task_by_id(task_id)
                print(f"Task with ID {task_id} was deleted successfully.")
            except ValueError:
                print("Please enter a valid number for ID.")

        elif choice == "6":
            # manager.save_to_file("tasks.json")
            print("Data saved. Goodbye!")
            manager.close_connection()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
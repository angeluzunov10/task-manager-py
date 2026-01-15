from models import PersonalTask, WorkTask
from task_manager import TaskManager

def main():
    manager = TaskManager()
    manager.load_from_file("tasks.json")

    while True:
        print("\n--- Task Manager Menu ---")
        print("1. Add Work Task")
        print("2. Add Personal Task")
        print("3. List All Tasks")
        print("4. Mark Task as Completed")
        print("5. Save and Exit")

        choice = input("Select an option (1-5): ")

        if choice == "1":
            # Тук събери вход за WorkTask
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            deadline = input("Enter task deadline (YYYY-MM-DD): ")

            task = WorkTask(title, description, deadline)
            manager.add_task(task)
            print(f"Work task '{title}' added.")
        elif choice == "2":
            # Тук събери вход за PersonalTask
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            priority = input("Enter task priority (Low/Medium/High): ")
            task = PersonalTask(title, description, priority)
            manager.add_task(task)
            print(f"Personal task '{title}' added.")
        elif choice == "3":
            manager.list_tasks()
        elif choice == "4":
            title = input("Enter the title of the task to complete: ")
            # Използвай manager.find_task_by_title и task.complete_task()
            task = manager.find_task_by_title(title)
            if task:
                task.complete_task()
                print(f"Task '{title}' marked as completed.")
            else:
                print(f"Task '{title}' not found.")
        elif choice == "5":
            manager.save_to_file("tasks.json")
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
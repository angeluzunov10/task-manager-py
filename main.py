from models import PersonalTask, WorkTask
from task_manager import TaskManager

manager = TaskManager()

t1 = WorkTask("Fix Bugs", "Fix the login issue", "2023-10-25")
t2 = PersonalTask("Gym", "Leg day", "High")

manager.add_task(t1)
manager.add_task(t2)    

print("--- All Tasks ---")
manager.list_tasks()

task = manager.find_task_by_title("Fix Bugs")
if task:
    task.complete_task()

print("\n--- After Completion ---")
manager.list_tasks()

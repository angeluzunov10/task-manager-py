from models import PersonalTask, WorkTask
from task_manager import TaskManager

manager = TaskManager()

# # t1 = WorkTask("Fix Bugs", "Fix the login issue", "2023-10-25")
# t2 = PersonalTask("Gym", "Leg day", "High")

# manager.add_task(t1)
# manager.add_task(t2)    

# manager.load_from_file("tasks.json")
# manager.list_tasks()

print("--- All Tasks ---")
manager.list_tasks()

task = manager.find_task_by_title("Fix Bugs")
if task:
    task.complete_task()

print("\n--- After Completion ---")
manager.list_tasks()

# print(t1.to_dict())
# print(t2.to_dict())

manager.save_to_file("tasks.json")


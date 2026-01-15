from models import PersonalTask, WorkTask
from task_manager import TaskManager

manager = TaskManager()
# Зареждаме съществуващите задачи още при стартиране
manager.load_from_file("tasks.json")

while True:
    pass
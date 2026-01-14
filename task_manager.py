from models import BaseTask, PersonalTask, WorkTask

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task: BaseTask):
        self.tasks.append(task)
    
    def list_tasks(self):
        for task in self.tasks:
            print(task)
    
    def find_task_by_title(self, title):
        for task in self.tasks:
            if task.title == title:
                return task
        return None
    

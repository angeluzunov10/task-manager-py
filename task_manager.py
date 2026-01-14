from models import BaseTask, PersonalTask, WorkTask
import json

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
    
    def save_to_file(self, filename):
        # правим списък от речници (тъй като не можем директно да сериализираме обекти)
        list_of_dicts = [task.to_dict() for task in self.tasks]

        # отвори файл за писане ('w') и запиши сериализирания json
        with open(filename, 'w') as f:
            # взима python обект (list_of_dicts), изсипва го във файлов обект (f) като го прави четим с space-ове (indent=4)
            json.dump(list_of_dicts, f, indent=4)
    

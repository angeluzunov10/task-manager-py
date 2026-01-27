from models import BaseTask, PersonalTask, WorkTask
import json
from database import SessionLocal
import models

class TaskManager:
    def __init__(self):
        self.tasks = [] # това вече не ни е нужно, защото ще ползваме база данни
        self.db = SessionLocal()  # Създаваме сесия за работа с базата данни

    def add_task(self, task):
        try:
            self.db.add(task)   # добавяме задачата в сесията
            self.db.commit()  # записваме промените в базата данни
            self.db.refresh(task)  # обновяваме обекта с данните от базата (напр. ID)
            print(f"Task '{task.title}' added to the database.")

        except Exception as e:
            self.db.rollback() # ако има грешка, връщаме промените
            print(f"Error saving task: {e}")
    
    def list_tasks(self):
        # SELECT * FROM tasks
        tasks = self.db.query(BaseTask).all()
        if not tasks:
            print("No tasks found in database.")

        for task in tasks:
            print(task)
    
    def get_all_tasks(self):
        return self.db.query(models.BaseTask).all()
    
    def find_task_by_title(self, title):
        # SELECT * FROM tasks WHERE title=title LIMIT 1
        return self.db.query(BaseTask).filter(BaseTask.title == title).first()
    
    def delete_task(self, title):
        task = self.find_task_by_title(title)
        if task:
            self.db.delete(task)
            self.db.commit()
            print(f"Task '{title}' deleted.")
        else:
            print(f"Task not found.")
    
    def get_task_by_id(self, task_id):
        return self.db.query(BaseTask).filter(BaseTask.id == task_id).first()
    
    def delete_task_by_id(self, task_id):
        task = self.db.query(BaseTask).filter(BaseTask.id == task_id).first()

        if task:
            self.db.delete(task)
            self.db.commit()
            print(f"Task with ID '{task_id}' was deleted successfully.")
            return True
        
        print(f"Task with ID '{task_id}' not found.")
        return False
    
    def close_connection(self):
        self.db.close()

    # def save_to_file(self, filename):
    #     # правим списък от речници (тъй като не можем директно да сериализираме обекти)
    #     list_of_dicts = [task.to_dict() for task in self.tasks]

    #     # отвори файл за писане ('w') и запиши сериализирания json
    #     with open(filename, 'w') as f:
    #         # взима python обект (list_of_dicts), изсипва го във файлов обект (f) като го прави четим с space-ове (indent=4)
    #         json.dump(list_of_dicts, f, indent=4)
    
    # def load_from_file(self, filename):
    #     try:
    #         with open(filename, 'r') as f:
    #             data = json.load(f)

    #             # използваме BaseTask static method from_dict за да създадем обекти от речниците
    #             self.tasks = [BaseTask.from_dict(d) for d in data]
        
    #     except FileNotFoundError:
    #         print(f"File {filename} not found. Starting with an empty task list.")
    #         self.tasks = []
    

class BaseTask:
    def __init__(self, title, description):
        self.__status = 'Pending'
        self.title = title
        self.description = description

    def get_status(self):
        return self.__status
    
    def complete_task(self):
        self.__status = 'Completed'

    def to_dict(self):          # сериализираме обекта в json формат
        return {
            'title': self.title,
            'description': self.description,
            'status': self.get_status(), # това е private променлива, затова използваме метода get_status()
            'type': self.__class__.__name__ # връща името на класа, тоест дали е WorkTask или PersonalTask
        }

    def __str__(self):
        return f"[{self.__status}] {self.title}"
    
class WorkTask(BaseTask):
    def __init__(self, title, description, deadline):
        super().__init__(title, description)
        self.deadline = deadline
    
    def to_dict(self):
        data = super().to_dict()
        data['deadline'] = self.deadline
        return data
    
    def __str__(self):
        return super().__str__() + f" (Deadline: {self.deadline})"

class PersonalTask(BaseTask):
    def __init__(self, title, description, priority):
        super().__init__(title, description)
        self.priority = priority

    def to_dict(self):  # сериализираме обекта в json формат 
        data = super().to_dict()
        data["priority"] = self.priority
        return data
    
    def __str__(self):
        return super().__str__() + f" (Priority: {self.priority})"

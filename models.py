class BaseTask:
    def __init__(self, title, description):
        self.__status = 'Pending'
        self.title = title
        self.description = description

    def get_status(self):
        return self.__status
    
    def complete_task(self):
        self.__status = 'Completed'

    def __str__(self):
        return f"[{self.__status}] {self.title}"
    
class WorkTask(BaseTask):
    def __init__(self, title, description, deadline):
        super().__init__(title, description)
        self.deadline = deadline
    
    def __str__(self):
        return super().__str__() + f" (Deadline: {self.deadline})"

class PersonalTask(BaseTask):
    def __init__(self, title, description, priority):
        super().__init__(title, description)
        self.priority = priority
    
    def __str__(self):
        return super().__str__() + f" (Priority: {self.priority})"

from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship # за връзки между обектите/таблиците


class BaseTask(Base): # наследяваме от Base, който е в database.py, за да може SQLAlchemy да работи с този клас(модела се прави от базата)
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True) # уникален идентификатор за всяка задача PK
    title = Column(String, index=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id")) # Това е външен ключ, който сочи към id-то в таблицата users
    status = Column(String, default='Pending') # сменяме го така, защото вече не е private променлива, а SQLAlchemy колонка
    type = Column(String) # за да различаваме типовете задачи (WorkTask, PersonalTask)

    # Специфични полета за наследниците
    deadline = Column(String, nullable=True)
    priority = Column(String, nullable=True)

    # Връзка: Всяка задача принадлежи на един потребител, а relationship ни позволява да достъпим потребителя чрез task.owner
    owner = relationship("User", back_populates="tasks")

    @staticmethod
    def from_dict(data):
        task_type = data.get('type')
        if task_type == 'WorkTask':
            task = WorkTask(
                title = data.get('title'),
                description = data.get('description'),
                deadline = data.get('deadline'),
                type = 'WorkTask'
            )
        elif task_type == 'PersonalTask':
            task = PersonalTask(
                title = data.get('title'),
                description = data.get('description'),
                priority = data.get('priority'),
                type = 'PersonalTask'
            )
        else:
            task = BaseTask(
                title = data.get('title'),
                description = data.get('description'),
                type = 'BaseTask'
            )

        # връщаме статуса, който е бил записан
        if data.get('status') == 'Completed':
            task.complete_task()
        return task


    # def __init__(self, title, description):       това вече не е нужно, защото SQLAlchemy се грижи за инициализацията
    #     self.__status = 'Pending'
    #     self.title = title
    #     self.description = description 

    def get_status(self):
        return self.status
    
    def complete_task(self):
        self.status = 'Completed'

    def to_dict(self):          # сериализираме обекта в json формат
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            # 'status': self.get_status(), # това е private променлива, затова използваме метода get_status()
            'status': self.status, # сменяме го така, защото вече не е private променлива, а SQLAlchemy колонка
            'type': self.type if self.type else self.__class__.__name__ # връща името на класа, тоест дали е WorkTask или PersonalTask
        }

    def __str__(self):
        # return f"[{self.__status}] {self.title}"
        return f"[{self.status}] {self.title}"
    
    
class WorkTask(BaseTask):
    # def __init__(self, title, description, deadline):
    #     super().__init__(title, description)
    #     self.deadline = deadline
    
    def to_dict(self):
        data = super().to_dict()
        data['deadline'] = self.deadline
        return data
    
    def __str__(self):
        return super().__str__() + f" (Deadline: {self.deadline})"

class PersonalTask(BaseTask):
    # def __init__(self, title, description, priority):
    #     super().__init__(title, description)
    #     self.priority = priority

    def to_dict(self):  # сериализираме обекта в json формат 
        data = super().to_dict()
        data["priority"] = self.priority
        return data
    
    def __str__(self):
        return super().__str__() + f" (Priority: {self.priority})"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String) # никога не съхраняваме пароли в plain text!

    # Връзка: Един потребител има много задачи
    # back_populates казва на SQLAlchemy как се казва атрибутът в другия модел
    tasks = relationship("BaseTask", back_populates="owner")


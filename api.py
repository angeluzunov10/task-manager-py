from fastapi import Body, FastAPI, HTTPException
import models # Добавяме това, за да имаме достъп до моделите
from task_manager import TaskManager

app = FastAPI()
manager = TaskManager()

# endpoint за началната страница
@app.get("/")
def home():
    return {"message": "Welcome to my Task Manager API!"}

# endpoint за извличане на всички задачи
@app.get("/tasks")
def get_all_tasks():
    # Тук използваме директно заявка към базата през нашия мениджър
    tasks = manager.db.query(models.BaseTask).all()
    return [task.to_dict() for task in tasks]

# endpoint за създаване на WorkTask
@app.post("/tasks/work")
def create_work_task(
    title: str = Body(...), # Body(...) указва, че тези параметри идват от тялото на заявката(това, което клиентът попълва във формата)
    description: str = Body(...),
    deadline: str = Body(...),
):
    new_task = models.WorkTask(title=title, description=description, deadline=deadline, type="WorkTask")
    manager.add_task(new_task)
    return {"message": "Work task created successfully", "task": new_task.to_dict()}

# endpoint за създаване на PersonalTask
@app.post("/tasks/personal")
def create_personal_task(
    title: str = Body(...),
    description: str = Body(...),
    priority: str = Body(...),
):
    new_task = models.PersonalTask(title=title, description=description, priority=priority, type="PersonalTask")
    manager.add_task(new_task)
    return {"message": "Personal task created successfully", "task": new_task.to_dict()}

# endpoint за изтриване на задача по ID
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    success = manager.delete_task_by_id(task_id)
    if not success:
        # FastAPI автоматично връща статус код 404 ако задачата не е намерена и програмата не се срива. Error Handling!
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"status": "deleted", "id": task_id}

# endpoint за ъпдейт на задача по ID
@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    title: str = Body(None),            # Тук е Body(None), защото тези полета са опционални при ъпдейт, т.е. може да се ъпдейтне само едно от тях
    description: str = Body(None),
    status: str = Body(None)
):
    # Намираме задачата по ID
    task = manager.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Ъпдейтваме полетата, които са подадени
    if title:
        task.title = title
    if description:
        task.description = description
    if status:
        task.status = status
    
    manager.db.commit()  # Запазваме промените в базата
    manager.db.refresh(task)  # Обновяваме обекта с новите данни от базата

    return {"status": "updated", "task": task.to_dict()}



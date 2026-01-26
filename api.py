from fastapi import Body, FastAPI, HTTPException
import models # Добавяме това, за да имаме достъп до моделите
from task_manager import TaskManager
from schemas import TaskCreate, TaskResponse, TaskUpdate

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

@app.post("/tasks", response_model=TaskResponse)
def create_task(task_data: TaskCreate):
    # проверяваме типа на задачата и създаваме съответния модел
    if task_data.deadline:
        new_task = models.WorkTask(
            title=task_data.title,
            description=task_data.description,
            deadline=task_data.deadline,
            type='WorkTask'
        )
    elif task_data.priority:
        new_task = models.PersonalTask(
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            type='PersonalTask'
        )

    # ако няма deadline или priority, хвърляме грешка
    else:
        raise HTTPException(
            status_code=400,
            detail="You must provide either a deadline for Work Task or a priority for Personal Task."
        )

    manager.add_task(new_task)
    return new_task


# ако имаме отделни POST ендпойнти за създаване на различни типове задачи, можем да ги дефинираме така:
# # endpoint за създаване на WorkTask
# @app.post("/tasks/work")
# def create_work_task(
#     title: str = Body(...), # Body(...) указва, че тези параметри идват от тялото на заявката(това, което клиентът попълва във формата)
#     description: str = Body(...),
#     deadline: str = Body(...),
# ):
#     new_task = models.WorkTask(title=title, description=description, deadline=deadline, type="WorkTask")
#     manager.add_task(new_task)
#     return {"message": "Work task created successfully", "task": new_task.to_dict()}

# # endpoint за създаване на PersonalTask
# @app.post("/tasks/personal")
# def create_personal_task(
#     title: str = Body(...),
#     description: str = Body(...),
#     priority: str = Body(...),
# ):
#     new_task = models.PersonalTask(title=title, description=description, priority=priority, type="PersonalTask")
#     manager.add_task(new_task)
#     return {"message": "Personal task created successfully", "task": new_task.to_dict()}

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
def update_task(task_id: int, task_update: TaskUpdate):
    task = manager.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # превръщаме Pydantic модела в речник, като пропускаме непопълнените полета
    update_data = task_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task, key, value) # динамично задаваме новите стойности на полетата
    
    manager.db.commit() # запазваме промените в базата
    manager.db.refresh(task) # обновяваме обекта с новите данни от базата
    return task





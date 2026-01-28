from fastapi import Body, FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse # <- Ново
from fastapi.staticfiles import StaticFiles # <- Ново
from fastapi.templating import Jinja2Templates # <- Ново
from typing import List # За списъците в response_model
import models # Добавяме това, за да имаме достъп до моделите
from task_manager import TaskManager
from schemas import TaskCreate, TaskResponse, TaskUpdate, UserCreate, UserResponse
from task_manager_app.auth import HashHandler

app = FastAPI()

# Къде са CSS/JS файловете (еквивалент на STATIC_URL в Django)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Къде са HTML файловете (еквивалент на TEMPLATES 'DIRS' в Django)
templates = Jinja2Templates(directory="templates")

manager = TaskManager()



# endpoint за началната страница с HTML отговор
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    # Взимаме всички задачи от базата
    tasks = manager.get_all_tasks() 
    # Връщаме template response (точно както render() в Django)
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

# endpoint за началната FastAPI страница
# @app.get("/")
# def home():
#     return {"message": "Welcome to my Task Manager API!"}

# endpoint за извличане на всички задачи (без Pydantic модел)
# @app.get("/tasks")
# def get_all_tasks():
#     # Тук използваме директно заявка към базата през нашия мениджър
#     tasks = manager.db.query(models.BaseTask).all()
#     return [task.to_dict() for task in tasks]

@app.get("/edit/{task_id}", response_class=HTMLResponse)
def edit_task_page(request: Request, task_id: int):
    # Предаваме task_id на шаблона, за да знае JS кое ID да търси по-късно.
    return templates.TemplateResponse("edit.html", {"request": request, "task_id": task_id})

# Извличане на всички задачи (с Pydantic модел)
@app.get("/tasks", response_model=List[TaskResponse])
def get_all_tasks():
    return manager.get_all_tasks()

# endpoint за извличане на определена задача
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    task = manager.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

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

# # endpoint за ъпдейт на задача по ID (без Pydantic модел)
# @app.put("/tasks/{task_id}")
# def update_task(task_id: int, task_update: TaskUpdate):
#     task = manager.get_task_by_id(task_id)
#     if not task:
#         raise HTTPException(status_code=404, detail="Task not found")
    
#     # превръщаме Pydantic модела в речник, като пропускаме непопълнените полета
#     update_data = task_update.model_dump(exclude_unset=True)

#     for key, value in update_data.items():
#         setattr(task, key, value) # динамично задаваме новите стойности на полетата
    
#     manager.db.commit() # запазваме промените в базата
#     manager.db.refresh(task) # обновяваме обекта с новите данни от базата
#     return task

# endpoint за ъпдейт на задача (Partial update с Pydantic V2)
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate):
    task = manager.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Взимаме само полетата, които са изпратени в заявката
    update_data = task_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task, key, value)
    
    manager.db.commit()
    manager.db.refresh(task)
    return task

@app.post("/register", response_model=UserResponse)
def register_user(user_data: UserCreate):
    # 1.Проверяваме дали потребителското име вече съществува
    existing_user = manager.db.query(models.User).filter(models.User.username == user_data.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # 2. Хешираме паролата
    hashed_password = HashHandler.hash_password(user_data.password)

    # 3.Създаваме нов потребител
    new_user = models.User(
        username=user_data.username,
        password=hashed_password
    )

    manager.db.add(new_user)
    manager.db.commit()
    manager.db.refresh(new_user)

    return new_user
    
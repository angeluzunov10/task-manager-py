from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from typing import List
import os

# Импортираме нашите неща със съответните пътища
from app.models.task_manager import TaskManager
from app.schemas.schemas import TaskCreate, TaskResponse, TaskUpdate
import app.models.models as models # Добавяме това, за да имаме достъп до моделите
from fastapi.templating import Jinja2Templates

from app.dependencies import get_current_user

# Настройваме шаблоните спрямо новата папка app/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Създаваме рутера
router = APIRouter(tags=["tasks"])
manager = TaskManager()

@router.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    # Преди тук вадехме токена ръчно. Вече няма нужда!
    
    try:
        # Подаваме целия request обект на функцията
        user = get_current_user(request)
        
        # Ако горното не хвърли грешка, значи имаме потребител
        # ЛОГИКА ЗА ФИЛТРИРАНЕ:
        # Използваме .filter() с оператор "ИЛИ" (|)
        # Искаме задачи, които са 'WorkTask' ИЛИ такива, чийто owner_id съвпада с текущия потребител
        tasks = manager.db.query(models.BaseTask).filter(
            (models.BaseTask.type == 'WorkTask') | 
            (models.BaseTask.owner_id == user.id)
        ).all()
        
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "tasks": tasks, 
            "user": user 
        })
    except Exception as e:
        # Тук влизаме, ако get_current_user вдигне HTTPException (няма токен или е невалиден)
        print(f"Auth error: {e}")
        return templates.TemplateResponse("landing.html", {"request": request, "user": None})
    
@router.get("/edit/{task_id}", response_class=HTMLResponse)
def edit_task_page(request: Request, task_id: int):
    user = get_current_user(request)
    task = manager.get_task_by_id(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Задачата не е намерена")
    
    # ЛОГИКА ЗА ДОСТЪП:
    # 1. Администратор може всичко.
    # 2. Потребител може да редактира САМО своите PersonalTask.
    can_edit = (
        user.role == "admin" or 
        (task.type == "PersonalTask" and task.owner_id == user.id)
    )

    if not can_edit:
        raise HTTPException(status_code=403, detail="Нямате права да редактирате тази задача")
    
    return templates.TemplateResponse("edit.html", {
        "request": request,
        "task_id": task.id,
        "user": user
    })


@router.get("/tasks", response_model=List[TaskResponse])
def get_all_tasks():
    return manager.get_all_tasks()

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    task = manager.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/tasks", response_model=TaskResponse)
def create_task(task_data: TaskCreate, user=Depends(get_current_user)):
    if task_data.deadline:
        new_task = models.WorkTask(
            title=task_data.title,
            description=task_data.description,
            deadline=task_data.deadline,
            owner_id=user.id,
            type='WorkTask'
        )
    elif task_data.priority:
        new_task = models.PersonalTask(
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            owner_id=user.id,
            type='PersonalTask'
        )
    else:
        raise HTTPException(
            status_code=400,
            detail="You must provide either a deadline for Work Task or a priority for Personal Task."
        )

    manager.add_task(new_task)
    return new_task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, user=Depends(get_current_user)):
    task = manager.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if not (user.role == "admin" or (task.type == "PersonalTask" and task.owner_id == user.id)):
        raise HTTPException(status_code=403, detail="Нямате права за изтриване на тази задача")
    
    manager.delete_task(task)
    manager.db.commit()
    return {"status": "deleted", "id": task_id}

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, user=Depends(get_current_user)):
    task = manager.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if not (user.role == "admin" or (task.type == "PersonalTask" and task.owner_id == user.id)):
        raise HTTPException(status_code=403, detail="Нямате права за промяна на тази задача")
    
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
    
    manager.db.commit()
    manager.db.refresh(task)
    return task
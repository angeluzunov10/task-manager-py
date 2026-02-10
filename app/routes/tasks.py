from fastapi import APIRouter, Request, HTTPException, Body
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
    token = request.cookies.get("access_token")
    
    # Ако няма токен, предаваме user=None
    if not token:
        return templates.TemplateResponse("landing.html", {"request": request, "user": None})
    
    try:
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
        
        user = get_current_user(token)
        tasks = manager.get_all_tasks() 
        
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "tasks": tasks, 
            "user": user # Тук предаваме обекта
        })
    except Exception as e:
        print(f"Auth error: {e}")
        # При грешка също предаваме user=None
        response = templates.TemplateResponse("landing.html", {"request": request, "user": None})
        response.delete_cookie("access_token")
        return response

@router.get("/edit/{task_id}", response_class=HTMLResponse)
def edit_task_page(request: Request, task_id: int):
    return templates.TemplateResponse("edit.html", {"request": request, "task_id": task_id})

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
def create_task(task_data: TaskCreate):
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
    else:
        raise HTTPException(
            status_code=400,
            detail="You must provide either a deadline for Work Task or a priority for Personal Task."
        )

    manager.add_task(new_task)
    return new_task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    success = manager.delete_task_by_id(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "deleted", "id": task_id}

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate):
    task = manager.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
    
    manager.db.commit()
    manager.db.refresh(task)
    return task
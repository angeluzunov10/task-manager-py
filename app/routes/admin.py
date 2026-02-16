from fastapi import APIRouter, Depends, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os

import app.models.models as models
from app.models.task_manager import TaskManager
from app.dependencies import get_admin_user

router = APIRouter(prefix="/admin", tags=["admin"])
manager = TaskManager()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@router.get("/dashboard", response_class=HTMLResponse)
def admin_dashboard(request: Request, user=Depends(get_admin_user)):
    # Взимаме всички данни директно от базата през мениджъра
    all_users = manager.db.query(models.User).all()
    all_tasks = manager.db.query(models.BaseTask).all()
    
    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request, 
        "user": user,
        "users": all_users,
        "tasks": all_tasks
    })

@router.post("/user/{user_id}/role")
def change_user_role(user_id: int, new_role: str = Form(...), user=Depends(get_admin_user)):
    target_user = manager.db.query(models.User).filter(models.User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404)
    
    if target_user.id == 1:
        raise HTTPException(status_code=400, detail="Root admin protection active.")
    
    target_user.role = new_role
    manager.db.commit()
    return RedirectResponse(url="/admin/dashboard", status_code=303)

@router.post("/user/{user_id}/delete")
def admin_delete_user(user_id: int, user=Depends(get_admin_user)):
    if user_id == 1:
        raise HTTPException(status_code=400, detail="Root admin protection active.")
    
    target_user = manager.db.query(models.User).filter(models.User.id == user_id).first()
    if target_user:
        manager.db.delete(target_user)
        manager.db.commit()
    return RedirectResponse(url="/admin/dashboard", status_code=303)
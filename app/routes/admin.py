from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from app.dependencies import RoleChecker
from app.models.models import UserRole

router = APIRouter(prefix="/admin", tags=["admin"])

# Път към шаблоните
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Само ADMIN може да влиза тук
allow_admin = RoleChecker([UserRole.ADMIN])

@router.get("/dashboard", response_class=HTMLResponse)
def admin_dashboard(request: Request, user=Depends(allow_admin)):
    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request, 
        "user": user
    })
from fastapi import HTTPException, Depends, status
from jose import jwt, JWTError
import os
from app.models.models import User, UserRole
from app.models.task_manager import TaskManager

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

manager = TaskManager()

def get_current_user(token: str):
    # Валидира JWT токена и връща текущия потребител 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    user = manager.db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        # Проверяваме дали ролята на потребителя е в списъка с разрешени роли
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=403, 
                detail="You do not have the required permissions"
            )
        return user
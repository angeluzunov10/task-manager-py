from dotenv import load_dotenv
from fastapi import HTTPException, Depends, Request, status
from jose import jwt, JWTError
import os
from app.models.models import User, UserRole
from app.models.task_manager import TaskManager

load_dotenv()  # Зареждаме .env файла, за да имаме достъп до променливите на средата

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

manager = TaskManager()

def get_current_user(request: Request):  # Вече приема целия Request обект
    # 1. Взимаме токена директно от бисквитките на браузъра
    token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Не сте влезли в профила си"
        )

    # 2. Махаме "Bearer ", ако присъства в бисквитката
    if token.startswith("Bearer "):
        token = token.replace("Bearer ", "")

    # 3. Валидираме JWT токена
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    # 4. Намираме потребителя в базата
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
    
def get_admin_user(user: User = Depends(get_current_user)):
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Достъпът е забранен. Изискват се администраторски права.")
    return user
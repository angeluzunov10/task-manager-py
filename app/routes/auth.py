from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from app.schemas.schemas import UserCreate, UserResponse
import app.models.models as models
from app.models.task_manager import TaskManager
from fastapi.templating import Jinja2Templates
import os
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

# Настройки за сигурност
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Настройваме шаблоните
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

router = APIRouter(tags=["auth"])
manager = TaskManager()

# --- КЛАСОВЕ ЗА СИГУРНОСТ (запазени) ---
class HashHandler:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

class TokenHandler:
    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- ЕНДПОИНТИ ---
@router.post("/register", response_model=UserResponse)
def register_user(user_data: UserCreate):
    existing_user = manager.db.query(models.User).filter(models.User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    hashed_password = HashHandler.hash_password(user_data.password)
    new_user = models.User(username=user_data.username, hashed_password=hashed_password)
    manager.db.add(new_user)
    manager.db.commit()
    manager.db.refresh(new_user)
    return new_user

@router.get("/register", response_class=HTMLResponse)
def get_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login_user(user_data: UserCreate):
    user = manager.db.query(models.User).filter(models.User.username == user_data.username).first()
    if not user or not HashHandler.verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = TokenHandler.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
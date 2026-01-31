from datetime import datetime, timedelta
import os
from jose import jwt
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")  # Зареждаме секретния ключ от .env файла
ALGORITHM = os.getenv("ALGORITHM")  # Алгоритъм за подписване на JWT токени
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))  # Време на изтичане на токена в минути

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Създаваме контекст за хеширане на пароли с bcrypt алгоритъм(най-сигурния стандарт към момента)

class HashHandler:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)  # превръщаме паролата в хеширана форма
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)  # проверяваме дали дадена парола съответства на хешираната форма

class TokenHandler:
    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()

        # Тук поставяме срок на изтичане на токена
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        
        # Подписваме токена със SECRET_KEY и връщаме токена
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
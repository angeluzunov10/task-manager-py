from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Създаваме контекст за хеширане на пароли с bcrypt алгоритъм(най-сигурния стандарт към момента)

class HashHandler:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)  # превръщаме паролата в хеширана форма
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)  # проверяваме дали дадена парола съответства на хешираната форма
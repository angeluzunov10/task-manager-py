from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Път към базата данни (в случая локален файл)
DATABASE_URL = "sqlite:///./tasks.db"

# 2. Engine - това е двигателят, който говори с DB
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 3. SessionLocal - всяка инстанция ще е една "сесия" (разговор) с базата
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base - от този клас ще наследяваме нашите модели (таблици)
Base = declarative_base()
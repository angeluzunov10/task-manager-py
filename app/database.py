from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Път към базата данни (в случая локален файл)
DATABASE_URL = "sqlite:///./tasks.db"

# 2. Engine - това е библиотеката, която знае как да "говори" със специфичната база (SQLite, Postgres).
#    Давам му адреса, а той се грижи за техническото свързване.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) # check_same_thread е необходимо за SQLite да позволи множество нишки
                                                                                # FastAPI работи с множество нишки автоматично

# 3. SessionLocal - всяка инстанция ще е една "сесия" (разговор) с базата
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base - от този клас ще наследяваме нашите модели (таблици)
# Това е "родителят" на всички таблици.
# SQLAlchemy го ползва като регистър. 
# Когато напишем class Task(Base), този обект Base си записва: "Аха, имам нова таблица със заглавие и статус".
# Без него create_all() нямаше да знае какво да създаде.
Base = declarative_base()
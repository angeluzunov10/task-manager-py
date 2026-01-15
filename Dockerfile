# 1. Базов образ с Python
FROM python:3.11-slim

# 2. Задаваме работна директория в контейнера
WORKDIR /app

# 3. Копираме requirements първо (за по-бързо билдване чрез кеш)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Копираме целия ни проект
COPY . .

# 5. Командата, която ще се изпълни при стартиране
CMD ["python", "main.py"]
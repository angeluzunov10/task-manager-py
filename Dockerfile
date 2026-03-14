# 1. Използваме лек образ на Python 3.12
FROM python:3.12-slim

# 2. Настройваме работната папка вътре в контейнера
WORKDIR /app

# 3. Копираме requirements.txt и инсталираме библиотеките
# Правим го преди копирането на останалия код за по-бърз build (cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Копираме цялото съдържание на проекта в контейнера
COPY . .

# 5. Казваме на FastAPI на кой порт да работи (Azure App Service обикновено ползва 80 или 8000)
EXPOSE 8000

# 6. Командата, която стартира приложението
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
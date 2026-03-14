FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Казваме на Python изрично къде да гледа
ENV PYTHONPATH=/app
EXPOSE 8000
# Използваме директен път до обекта app
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
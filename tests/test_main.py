from fastapi.testclient import TestClient
# Внасяме твоя FastAPI обект. Промени 'app.main', ако твоят файл се казва по друг начин
from app.main import app 

# Създаваме клиент, който ще "разговаря" с нашето приложение
client = TestClient(app)

def test_homepage_status():
    response = client.get("/")
    assert response.status_code == 200

def test_create_task_protected():
    """Проверява, че нерегистриран потребител не може да създава задачи (401)."""
    payload = {"title": "Тест", "description": "...", "task_type": "Work", "due_date": "2026-12-31"}
    response = client.post("/tasks/", json=payload)
    
    # Потвърждаваме, че защитата ни работи!
    assert response.status_code == 401
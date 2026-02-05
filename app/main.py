from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from app.routes import tasks, auth
import app.models.models as models
from app.database import engine
import os

app = FastAPI(title="Task Master Pro")

# Създаваме таблиците
models.Base.metadata.create_all(bind=engine)

# Пътища
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# ВКЛЮЧВАМЕ РУТЕРИТЕ (Магията на APIRouter)
app.include_router(tasks.router)
app.include_router(auth.router)

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    file_path = os.path.join(BASE_DIR, "static", "favicon.ico")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return HTMLResponse(status_code=204) # Връщаме "No Content", ако нямаме иконка
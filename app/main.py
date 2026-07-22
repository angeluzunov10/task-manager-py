from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.routes import tasks, auth, admin
import app.models.models as models
from app.database import engine
import os

class HTTPSRedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Казваме на FastAPI да генерира линковете с https
        request.scope["scheme"] = "https"
        response = await call_next(request)
        return response

app = FastAPI(title="Task Master Pro")
app.add_middleware(HTTPSRedirectMiddleware)  # Принуждаваме HTTPS за по-голяма сигурност

# Създаваме таблиците
models.Base.metadata.create_all(bind=engine)
auth.create_initial_admin()

# Пътища
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
else:
    print("WARNING: Static directory not found!")

# ВКЛЮЧВАМЕ РУТЕРИТЕ (Магията на APIRouter)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(tasks.router)

@app.get('/favicon.ico', include_in_schema=False)   # include_in_schema=False за да не се показва в документацията
async def favicon():
    file_path = os.path.join(BASE_DIR, "static", "favicon.ico")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return HTMLResponse(status_code=204) # Връщаме "No Content", ако нямаме иконка
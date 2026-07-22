from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
import os

from app.routes import tasks, auth, admin
import app.models.models as models
from app.database import engine

# За да можем да различаваме средата, в която работим (development, production)
# правим тази проверка, за да можем да променяме поведението на приложението,
# в това число и зареждане на статични файлове, ако сме в production среда.

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

app = FastAPI(title="Task Master Pro")

# HTTPS Middleware – активира се САМО в production (напр. в облака), така кода ще ми работи и в development среда без да се налага да имам валиден SSL сертификат локално.
if ENVIRONMENT == "production":
    class HTTPSRedirectMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            request.scope["scheme"] = "https"
            response = await call_next(request)
            return response

    app.add_middleware(HTTPSRedirectMiddleware)

# Създаваме таблиците
models.Base.metadata.create_all(bind=engine)

# Създанаме първи администратор, ако няма такъв в базата данни
auth.create_initial_admin()

# Пътища за static
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
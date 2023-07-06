from fastapi import FastAPI
from fastapi import Depends, Response
from fastapi.staticfiles import StaticFiles
from fastapi import Request, status
from fastapi.responses import RedirectResponse
from routers.login import Login
from routers.usuarios import Usuarios
from routers.agenda import agenda
from routers.doctores import doctores
import uvicorn
from config import templates
from database.conexion import SessionLocal, engine
from database import models
from sqlalchemy.orm import Session
from manager import manager

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(Login)
app.include_router(Usuarios, prefix='/usuarios')
app.include_router(agenda, prefix='/agenda')
app.include_router(doctores, prefix='/doctores')
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.exception_handler(status.HTTP_404_NOT_FOUND)
async def ERROR_404(request: Request, _):
    return templates.TemplateResponse("404.html", context={"request": request},status_code=404)

@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
async def UNAUTHORIZED_401(request: Request, _):
    return RedirectResponse("/login")

@app.get('/')
async def index(request: Request, user=Depends(manager)):
    return templates.TemplateResponse('index.html', context={'request': request, 'userInfo': user})

@app.post('/')
async def index(request: Request, user=Depends(manager)):
    return templates.TemplateResponse('index.html', context={'request': request, 'userInfo': user})
if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0')
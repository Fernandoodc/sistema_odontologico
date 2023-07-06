from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm,  OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi import Request, Response
from fastapi import status
from fastapi import Form
from fastapi import Depends
from fastapi.responses import RedirectResponse
from werkzeug.security import generate_password_hash, check_password_hash
from config import settings
from manager import manager, query_user, controlAcceso
from database.conexion import get_db
from database.models import User
from sqlalchemy.orm import Session
from schemas.schemas import changePasw, Respuesta
from datetime import datetime, timedelta


templates = Jinja2Templates(directory="templates")

Login = APIRouter(tags=['login'])
@Login.get('/login', status_code=status.HTTP_401_UNAUTHORIZED)
async def login(request: Request):
    error = []
    return templates.TemplateResponse('login.html', context={'request': request, 'error': error}, status_code=status.HTTP_401_UNAUTHORIZED)

@Login.post('/login')
async def create_token(request: Request, response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    username = form_data.username
    password = form_data.password
    error = []
    try:
        user = query_user(username)
        if user != None:
            if check_password_hash(user['password'], password):
                access_token = manager.create_access_token(data={'sub': username})
                infoUser = db.query(User).filter(User.id == user['id']).first()
                #para saber si esta logeando y todavia no venció su sesion
                """if(infoUser.venc_login and infoUser.logeado):
                    if(infoUser.venc_login > datetime.now() and infoUser.logeado == True):
                        error.append('Ya tiene una sesión activa')
                        response.status_code = status.HTTP_401_UNAUTHORIZED
                        return templates.TemplateResponse('login.html', context={'request': request, 'error': error})"""
                infoUser.logeado = True
                infoUser.venc_login = datetime.now() + timedelta(hours=settings.VIDA_TOKEN)
                db.commit()
                db.refresh(infoUser)
                response = RedirectResponse('/')
                manager.set_cookie(response=response, token=access_token)
                return response
        error.append('Usuario o Contraseña Incorrecta')
        response.status_code = status.HTTP_401_UNAUTHORIZED
    except Exception as e:
        print(e)
        error.append('Ocurrió un error interno')
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return templates.TemplateResponse('login.html', context={'request': request, 'error': error})


@Login.get('/profile')
async def profile(request: Request, user=Depends(manager), db : Session = Depends(get_db)):
    usuario = db.query(User).filter(User.username == user.username).first()
    return templates.TemplateResponse('users-profile.html', context={'request': request, 'usuario': usuario, 'userInfo': user, 'infoUser': user})

@Login.put('/update_passw')
async def actualizarPassword(response: Response, pasw : changePasw, user=Depends(manager), db : Session = Depends(get_db)):
    usuario = query_user(user.username)
    if check_password_hash(usuario['password'], pasw.currentPasw):
        hash = generate_password_hash(pasw.newPasw, method=settings.HASH)
        #await update_one('usuarios', {'username': user.username}, {'$set': {'password': hash}})
        usuario = db.query(User).filter(User.username == user.username).first()
        usuario.password = hash
        db.commit()
        db.refresh(usuario)
        return {'msg': 'success'}
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {'msg': 'Contraseña incorrecta, intente de nuevo'}

@Login.get('/logout')
async def logout(request: Request ,response: Response, user=Depends(manager), db : Session = Depends(get_db)):
    error = []
    response =  templates.TemplateResponse('login.html', context={'request': request, 'error': error}, status_code=status.HTTP_401_UNAUTHORIZED)
    response.delete_cookie(key=settings.KEY_TOKEN)
    userInfo = db.query(User).filter(User.id == user.id).first()
    userInfo.logeado = False
    db.commit()
    return response
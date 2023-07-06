from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi import Request, Response
from fastapi import status
from fastapi import Depends
from schemas.schemas import datosUsuario, resetPasw, newUser, permisosUsers, newPasw
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from manager import	 manager
from config import settings
from sqlalchemy.orm import Session
from database.conexion import get_db
from database.models import User, Permisos
from manager import permisos, controlAcceso
from typing import List
Usuarios = APIRouter()

templates = Jinja2Templates(directory="templates")

@Usuarios.get('/')
async def listaUsuarios(request: Request, id:str='', user=Depends(manager), db : Session = Depends(get_db)):
    controlAcceso(user=user, typeRequired='4.1')
    users = db.query(User).filter(User.activo == True).all()
    return templates.TemplateResponse('usuarios.html', context={'request': request, 'usuarios': users, 'permisos': permisos, 'id':id,  'userInfo': user})


@Usuarios.get('/nuevo_usuario')
async def nuevoUsuario(request: Request, user=Depends(manager)):
    controlAcceso(user=user, typeRequired='4.1')
    return templates.TemplateResponse('nuevo_usuario.html', context={'request': request, 'permisos': permisos,  'userInfo': user})
@Usuarios.post('/new_user')
async def agregarUsuario(respose: Response, data:newUser, user=Depends(manager), db : Session = Depends(get_db)):
    controlAcceso(user=user, typeRequired='4.1')
    if db.query(User).filter(User.username == data.username).first() != None:
        respose.status_code = status.HTTP_409_CONFLICT
        return {'msg': 'Username ya se encuentra en uso'}
    hash = generate_password_hash(data.password, method=settings.HASH)
    data.password = hash
    newUser = User(username = data.username, password=data.password, nombre = data.nombre, apellido = data.apellido, direccion = data.direccion, celular = data.celular, email = data.email, documento = data.documento, activo = True)
    db.add(newUser)
    db.flush()
    db.refresh(newUser)
    for i in data.permisos:
        newPermiso = Permisos(id_usuario = newUser.id, codigo = i.codigo)
        db.add(newPermiso)
    db.commit()
    return {'msg': 'success'}


@Usuarios.get('/info')
async def infoUser(response: Response, id:str, user=Depends(manager), db : Session = Depends(get_db)):
    controlAcceso(user=user, typeRequired='4.1')
    info = db.query(User).filter(User.id == id).first()
    permisos = db.query(Permisos).filter(Permisos.id_usuario == id).all()
    return {
        'usuario': info,
        'permisos': permisos
    }


@Usuarios.put('/editar')
async def editarUsuario(respose: Response, id:str, datos:datosUsuario, user=Depends(manager), db : Session = Depends(get_db)):
    controlAcceso(user=user, typeRequired='4.1')
    usernameStatus = db.query(User).filter(User.username == datos.username, User.id != id).first()
    if usernameStatus != None:
        respose.status_code = status.HTTP_409_CONFLICT
        return {'msg': 'Username ya se encuentra en uso'}
    user = db.query(User).filter(User.id == id).first()
    user.documento = datos.documento
    user.nombre = datos.nombre
    user.apellido = datos.apellido
    user.celular = datos.celular
    user.email = datos.email
    user.direccion = datos.direccion
    db.commit()
    db.refresh(user)
    return {'msg': 'success'}


@Usuarios.get('/verif_username')
async def verificarUsername(respose: Response, username:str, id:str='', user=Depends(manager), db : Session = Depends(get_db)):
    controlAcceso(user=user, typeRequired='4.1')
    filtro = db.query(User).filter(User.username == username).first()
    if  filtro == None:
        return {'msg': 'username disponible'}
    else:
        respose.status_code = status.HTTP_409_CONFLICT
        return {'msg': 'username ya se encuentra en uso'}


@Usuarios.put('/change_type_user')
async def cambiaTipoUser(response: Response, idUser:str, newPermisos : List[permisosUsers]  ,user=Depends(manager), db : Session = Depends(get_db)):
    controlAcceso(user=user, typeRequired='4.1')
    permisosUser = db.query(Permisos).filter(Permisos.id_usuario == idUser).all()
    for i in permisosUser:
        db.delete(i)
        db.flush()
    for i in newPermisos:
        newPermiso = Permisos(id_usuario = idUser, codigo = i.codigo)
        db.add(newPermiso)
        db.flush()
    db.commit()
    return {'msg': 'success'}

@Usuarios.put('/reset_password')
async def resetPasword(response: Response, datos:resetPasw, user=Depends(manager), db : Session = Depends(get_db)):
    controlAcceso(user=user, typeRequired='4.1')
    paswHash = generate_password_hash(datos.newPassword, method=settings.HASH)
    usuario = db.query(User).filter(User.id == datos.userId).first()
    usuario.password = paswHash
    db.commit()
    db.refresh(usuario)
    return {'msg': 'success'}

@Usuarios.put('/act_password')
async def resetPasword(response: Response, datos:newPasw, user=Depends(manager), db : Session = Depends(get_db)):
    paswHash = generate_password_hash(datos.newPassword, method=settings.HASH)
    usuario = db.query(User).filter(User.id == datos.userId).first()
    if check_password_hash(usuario.password, datos.curretPasw):
        usuario.password = paswHash
        db.commit()
        db.refresh(usuario)
        return {'msg': 'success'}
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {'msg': 'Contraseña Incorrecta'}


@Usuarios.delete('/eliminar')
async def eliminarUsuario(respose: Response, id:str, user=Depends(manager), db : Session = Depends(get_db)):
    controlAcceso(user=user, typeRequired='4.1')
    user = db.query(User).filter(User.id == id).first()
    user.activo = False
    db.commit()
    return {'msg': 'success'}


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
from database.models import User, Permisos, Doctores, Especialidades
from manager import permisos, controlAcceso
from typing import List
doctores = APIRouter()

templates = Jinja2Templates(directory="templates")

@doctores.get('/')
async def listaUsuarios(request: Request, id:str='', user=Depends(manager), db : Session = Depends(get_db)):
    controlAcceso(user=user, typeRequired='4.2')
    doctores = db.query(User.id ,User.username, User.nombre, User.documento, User.activo, Doctores.registro, Especialidades.descripcion).join(User).join(Especialidades).all()
    drs = []
    for i in doctores:
        drs.append({
            'id': i[0],
            'username': i[1],
            'nombre': i[2],
            'documento': i[3],
            'activo': i[4],
            'registro': i[5],
            'especialidad': i[6]
        })
    return templates.TemplateResponse('doctores.html', context={'request': request, 'usuarios': drs, 'permisos': permisos, 'id':id,  'userInfo': user})


@doctores.get('/nuevo_usuario')
async def nuevoUsuario(request: Request, user=Depends(manager)):
    controlAcceso(user=user, typeRequired='4.2')
    return templates.TemplateResponse('nuevo_usuario.html', context={'request': request, 'permisos': permisos,  'userInfo': user})
@doctores.post('/new_user')
async def agregarUsuario(respose: Response, data:newUser, user=Depends(manager), db : Session = Depends(get_db)):
    controlAcceso(user=user, typeRequired='4.2')
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


@doctores.get('/info')
async def infoUser(response: Response, id:str, user=Depends(manager), db : Session = Depends(get_db)):
    controlAcceso(user=user, typeRequired='4.2')
    info = db.query(User).filter(User.id == id).first()
    permisos = db.query(Permisos).filter(Permisos.id_usuario == id).all()
    return {
        'usuario': info,
        'permisos': permisos
    }


@doctores.put('/editar')
async def editarUsuario(respose: Response, id:str, datos:datosUsuario, user=Depends(manager), db : Session = Depends(get_db)):
    controlAcceso(user=user, typeRequired='4.2')
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


@doctores.get('/verif_username')
async def verificarUsername(respose: Response, username:str, id:str='', user=Depends(manager), db : Session = Depends(get_db)):
    controlAcceso(user=user, typeRequired='4.2')
    filtro = db.query(User).filter(User.username == username).first()
    if  filtro == None:
        return {'msg': 'username disponible'}
    else:
        respose.status_code = status.HTTP_409_CONFLICT
        return {'msg': 'username ya se encuentra en uso'}


@doctores.put('/change_type_user')
async def cambiaTipoUser(response: Response, idUser:str, newPermisos : List[permisosUsers]  ,user=Depends(manager), db : Session = Depends(get_db)):
    controlAcceso(user=user, typeRequired='4.2')
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

@doctores.put('/reset_password')
async def resetPasword(response: Response, datos:resetPasw, user=Depends(manager), db : Session = Depends(get_db)):
    controlAcceso(user=user, typeRequired='4.2')
    paswHash = generate_password_hash(datos.newPassword, method=settings.HASH)
    usuario = db.query(User).filter(User.id == datos.userId).first()
    usuario.password = paswHash
    db.commit()
    db.refresh(usuario)
    return {'msg': 'success'}

@doctores.put('/act_password')
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


@doctores.delete('/eliminar')
async def eliminarUsuario(respose: Response, id:str, user=Depends(manager), db : Session = Depends(get_db)):
    controlAcceso(user=user, typeRequired='4.2')
    user = db.query(User).filter(User.id == id).first()
    user.activo = False
    db.commit()
    return {'msg': 'success'}


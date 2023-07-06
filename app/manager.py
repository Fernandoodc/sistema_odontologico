from fastapi_login import LoginManager
from fastapi import Response
from fastapi import HTTPException, status
from config import settings
from schemas.schemas import tokenUser
from datetime import timedelta, datetime
from database.conexion import SessionLocal
from database.models import User, Permisos

manager = LoginManager( settings.SECRET_KEY, '/login', use_cookie=True, use_header=True, default_expiry=timedelta(days=365), cookie_name=settings.KEY_TOKEN)
#listado de permisos, los cambios aca se ven reflejados en la vista de usuarios
permisos = [
    {
        'grupo': 'Agenda de Citas',
        'codigo': '1',
        'contenido':[
            {
                'codigo': '1.1',
                'descripcion': 'Ver, Agregar, editar, eliminar'
            },
        ]
    },
    {
        'grupo': 'Libro Diario',
        'codigo': '2',
        'contenido':[
            {
                'codigo': '2.1',
                'descripcion': 'Ver, Agregar, editar, eliminar'
            },
        ]
    },
    {
        'grupo': 'Informes',
        'codigo': '3',
        'contenido':[
            {
                'codigo': '3.3',
                'descripcion': 'Libro Diario'
            },
            {
                'codigo': '3.1',
                'descripcion': 'Libro Mayor'
            },
            {
                'codigo': '3.2',
                'descripcion': 'Sumas y Saldos'
            }
        ]
    },
    {
        'grupo': 'Ajustes',
        'codigo': '4',
        'contenido':[
            {
                'codigo': '4.1',
                'descripcion': 'Administrar Usuarios'
            },
            {
                'codigo': '4.2',
                'descripcion': 'Periodo Fiscal'
            }
        ]
    },
    {
        'grupo': 'Empresas',
        'codigo': '5',
        'contenido': [
            {
                'codigo': '5.1',
                'descripcion': 'Crear, Editar, Eliminar'
            }
        ]
    },
]
@manager.user_loader()
def get_user(username: str, response = Response):
    """
    Get a user from the db
    :param user_id: E-Mail of the user
    :return: None or the user object
    """
    try:
        session = SessionLocal()
        user = session.query(User).filter(User.username == username, User.activo == True).first()
        now = datetime.now()
        #control para saber si su token ya venció
        """if(user.venc_login):
            if(now > user.venc_login):# or user.logeado == False):
                #user.logeado = False
                #session.commit()
                session.close()
                return None"""
        #renovación de la vida del token
        user.venc_login = datetime.now() + timedelta(hours=settings.VIDA_TOKEN)
        session.commit()
        session.refresh(user)

        permisosUser = session.query(Permisos).filter(Permisos.id_usuario == user.id).all()
        listPermisos = []
        for i in permisosUser:
            listPermisos.append(i.codigo)
        #empresa = session.query(tEmpresas).filter(tEmpresas.id_empresa == user.id_empresa).first()
        info = tokenUser(id = user.id ,username=user.username, nombre=user.nombre, apellido=user.apellido, permisos=listPermisos)
        #token = manager.create_access_token(data={'sub': user.username, 'new': "yes"})
        session.close()
        #return manager.set_cookie(response=response, token=token)
        return info
    except Exception as e:
        print(e, "error")
        return None
    
def query_user(username: str):
    """
    Get a user from the db
    :param user_id: E-Mail of the user
    :return: None or the user object
    """
    try:
        session = SessionLocal()
        #return find_one('usuarios', {'username': username}, {'_id': 0,'username': 1, 'password': 1, 'codTipoUsuario': 1})
        user = session.query(User.id, User.username, User.password).filter(User.username == username, User.activo == True).first()
        if user == None:
            return None
        response = dict(zip(['id', 'username', 'password'], user))
        session.close()
        return response
    except Exception as e:
        print(e)
        return None

def controlAcceso(typeRequired, user):
        if(not typeRequired in user.permisos ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes los credenciales necesarios",
                headers={"WWW-Authenticate": "Bearer"},
            )
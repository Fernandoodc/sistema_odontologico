from typing import Optional
from pydantic import BaseModel
from datetime import date
from typing import List

class permisosUsers(BaseModel):
    codigo : str
class tokenUser(BaseModel):
    id : int
    username: str
    nombre: str
    apellido: str
    permisos: List[str]
class username(BaseModel):
    username: str
class datosUsuario(username):
    documento: str
    nombre: str
    apellido: str
    celular: str = ''
    email: str = ''
    direccion : str =''
class changePasw(BaseModel):
    currentPasw: str
    newPasw: str


class newUser(datosUsuario):
    password:str
    permisos : List[permisosUsers]
class resetPasw(BaseModel):
    userId: str
    newPassword: str

class newPasw(resetPasw):
    curretPasw : str

class Respuesta(BaseModel):
    msg: str
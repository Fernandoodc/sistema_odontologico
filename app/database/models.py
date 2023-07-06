from sqlalchemy import Column, Integer, String, Boolean, Date, Time , ForeignKey, DateTime
from database.conexion import Base
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
class User(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(300), nullable=False)
    nombre = Column(String(200), nullable=False)
    apellido = Column(String(200), nullable=False)
    direccion = Column(String(200))
    celular = Column(String(50))
    email = Column(String(100))
    documento = Column(String(30), nullable=False)
    activo = Column(Boolean, nullable=False)
    logeado = Column(Boolean)
    venc_login = Column(DateTime)
    id_tipo = Column(Integer, ForeignKey('tipos_usuarios.id_tipo'))

class TiposUsuarios(Base):
    __tablename__ = 'tipos_usuarios'
    id_tipo = Column(Integer, primary_key=True)
    descripcion = Column(String(30))

class Especialidades(Base):
    __tablename__ = 'especialidades'
    id_especialidad = Column(Integer, primary_key=True)
    descripcion = Column(String(100), nullable=False)

class Doctores(Base):
    __tablename__ = 'doctores'
    id_doctor = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    id_especialidad = Column(Integer, ForeignKey('especialidades.id_especialidad'), nullable=False)
    registro = Column(String(20), nullable=False)
    

class Permisos(Base):
    __tablename__ = 'permisos'
    id_permiso = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    codigo = Column(String(10))

class Pacientes(Base):
    __tablename__ = 'pacientes'
    id_paciente = Column(Integer, primary_key=True, index= True)
    documento = Column(String(20), index=True, unique=True)
    nombre = Column(String(50))
    apellido = Column(String(50))
    celular = Column(String(50))
    email = Column(String(100))
    direccion = Column(String(100))

class Citas(Base):
    __tablename__ = 'citas'
    id_cita = Column(Integer, primary_key=True)
    fecha = Column(Date)
    hora = Column(Time)
    duracion = Column(Integer)
    id_doctor = Column(Integer, ForeignKey('doctores.id_doctor'))
    id_paciente = Column(Integer, ForeignKey('pacientes.id_paciente'))

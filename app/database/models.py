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
    intervalo = Column(Integer, nullable=False)
    

class Permisos(Base):
    __tablename__ = 'permisos'
    id_permiso = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    codigo = Column(String(10))

class EstadosCiviles(Base):
    __tablename__ = 'estados_civiles'
    id_ec = Column(Integer, primary_key=True)
    descripcion = Column(String(25))

class Pacientes(Base):
    __tablename__ = 'pacientes'
    id_paciente = Column(Integer, primary_key=True, index= True)
    documento = Column(String(20), index=True, unique=True)
    nombre = Column(String(50))
    apellido = Column(String(50))
    nacimiento = Column(Date)
    sexo = Column(Boolean)
    id_ec = Column(Integer, ForeignKey('estados_civiles.id_ec'))
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
    asistio = Column(Boolean)

class Enfermedades(Base):
    __tablename__ = 'enfermedades'
    id_enfermedad = Column(Integer, primary_key=True)
    descripcion = Column(String(100), nullable=False)

class CausasPerdidas(Base):
    __tablename__ = 'cuasas_perdidas'
    id_causa = Column(Integer, primary_key=True)
    descripcion = Column(String(100), nullable=False)

class ElementosHigiene(Base):
    __tablename__ = 'elementos_higiene'
    id_elemento = Column(Integer, primary_key=True)
    descripcion = Column(String(100), nullable=False)

class CausasFaltaTrato(Base):
    __tablename__ = 'c_falta_trato'
    id_causa = Column(Integer, primary_key=True)
    descripcion = Column(String(100), nullable=False)

class Preguntas(Base):
    __tablename__ = 'preguntas'
    id_pregunta = Column(Integer, primary_key=True)
    pregunta = Column(String(100), nullable=False)
    sub_pregunta = Column(String(100), nullable=True)

class Respuestas(Base):
    __tablename__ = 'respuestas'
    id_pregunta = Column(Integer, ForeignKey('preguntas.id_pregunta'), primary_key=True)
    id_paciente = Column(Integer, ForeignKey('fichas.id_paciente'), primary_key=True)
    bol_respuesta = Column(Boolean) #respuesta de la pregunta principal, es un si o un no
    text_respuesta = Column(String(200), nullable=True)  #respuesta de la sub-pregunta

class CausasPerdidasPaciente(Base):
    __tablename__ = 'causas_paciente'
    id_causa = Column(Integer, ForeignKey('cuasas_perdidas.id_causa'), primary_key=True)
    id_paciente = Column(Integer, ForeignKey('fichas.id_paciente'), primary_key=True)

class CausasFaltaTratoPaciente(Base):
    __tablename__ = 'falta_trato_paciente'
    id_causa = Column(Integer, ForeignKey('c_falta_trato.id_causa'), primary_key=True)
    id_paciente = Column(Integer, ForeignKey('fichas.id_paciente'), primary_key=True)

class EnfermedadesPaciente(Base):
    __tablename__ = 'enf_paciente'
    id_enfermedad = Column(Integer, ForeignKey('enfermedades.id_enfermedad'), primary_key=True)
    id_paciente = Column(Integer, ForeignKey('fichas.id_paciente'), primary_key=True)

class ElementosHigienePaciente(Base):
    __tablename__ = 'elementos_paciente'
    id_elemento = Column(Integer, ForeignKey('elementos_higiene.id_elemento'), primary_key=True)
    id_paciente = Column(Integer, ForeignKey('fichas.id_paciente'), primary_key=True)

class Fichas(Base):
    __tablename__ = 'fichas'
    id_paciente = Column(Integer, ForeignKey('pacientes.id_paciente'), primary_key=True)
    fecha_act = Column(Date, nullable=True)
    embarazo = Column(Integer)
    tiempo_embarazo = Column(String(100))
    tol_anestesia = Column(Integer)
    test_elisa = Column(Integer)
    tiempo_telisa = Column(String(100))
    ult_consulta = Column(Integer)
    cepillado = Column(Integer)
    otro_elemento = Column(String(100))
    otro_enfermedad = Column(String(100))
    otro_falta_trato = Column(String(100))
    comentarios = Column(String(200))



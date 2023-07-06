from fastapi import APIRouter
from fastapi import Request, Response
from fastapi import status
from fastapi import Depends
from datetime import datetime, timedelta
from manager import	 manager
from config import settings, templates
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from database.conexion import get_db
from database.models import User
from manager import controlAcceso
from database.models import Doctores, Citas, Pacientes
from schemas.agenda import NewCita
from json import dumps
agenda = APIRouter()
@agenda.get('/')
async def viewAgenda(request: Request, fecha:str = datetime.now().strftime("%Y-%m-%d"), idDoctor:int = None,  user=Depends(manager), db : Session = Depends(get_db)):
    controlAcceso(user=user, typeRequired='1.1')
    pacientes = db.query(Pacientes).all()
    drs = db.query(Doctores.id_doctor, User.nombre, User.apellido).join(User).filter(User.id_tipo == 2, User.activo == True).all()
    if idDoctor == None:
        citas = db.query(Citas.hora, Citas.duracion, Pacientes.nombre, Pacientes.apellido, Pacientes.celular, User.nombre, User.apellido).join(Pacientes).join(Doctores).join(User).filter(Citas.fecha == fecha).all()
    return templates.TemplateResponse('agenda.html', context={'request': request, 'userInfo': user, 'fecha': fecha, 'doctores': drs, 'citas': citas, 'pacientes': pacientes})

@agenda.post('/citas/nuevo')
async def nuevaCita(request: Request, response: Response, datos: NewCita,  user=Depends(manager), db : Session = Depends(get_db)):
    controlAcceso(user=user, typeRequired='1.1')
    fecha = datetime.combine(datos.fecha, datos.hora)
    hora_fin =fecha + timedelta(minutes=datos.duracion)
    #trae todas la citas de ese día cuyo horario es menor a la cita actual
    citas_existentes = db.query(Citas).filter(
        Citas.id_doctor == datos.idDoctor,
        Citas.fecha == datos.fecha,
        Citas.hora <= fecha.time(),
    ).all()
    # Verifica si hay alguna superposición de horarios
    superpuesta = False
    for cita in citas_existentes:
        datosCita = datetime.combine(cita.fecha, cita.hora)
        if (datosCita + timedelta(minutes=cita.duracion)) > fecha:
            superpuesta = True
            break
    if superpuesta:
        response.status_code = status.HTTP_409_CONFLICT
        return "Horario no disponible, seleccione otra"
    else:
        newCita = Citas(id_paciente = datos.idPaciente, id_doctor = datos.idDoctor, fecha = datos.fecha, hora = datos.hora, duracion = datos.duracion)
        db.add(newCita)
        db.flush()
        db.refresh(newCita)
        infoCita = db.query(Citas.hora, Citas.duracion, Pacientes.nombre, Pacientes.apellido, Pacientes.celular, User.nombre, User.apellido).join(Pacientes).join(Doctores).join(User).filter(Citas.id_cita == newCita.id_cita).first()
        if infoCita:
            keys = infoCita._fields
            aux = dict(zip(keys, infoCita))
            return aux
        return infoCita
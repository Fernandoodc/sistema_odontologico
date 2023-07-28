from fastapi import APIRouter, Query
from fastapi import Request, Response
from fastapi import status
from fastapi import Depends
from datetime import datetime, timedelta
from manager import	 manager
from config import settings, templates
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from sqlalchemy import exc, insert
from sqlalchemy.sql import or_
from database.conexion import get_db
from manager import controlAcceso
from database.models import Pacientes, EstadosCiviles, Citas, Preguntas, ElementosHigiene, Enfermedades, CausasPerdidas, EnfermedadesPaciente, CausasPerdidasPaciente, ElementosHigienePaciente, Respuestas, Fichas, CausasFaltaTrato, CausasFaltaTratoPaciente
from schemas.pacientes import NuevoPaciente
from schemas.ficha import NewFicha
from funciones import edadPaciente
from json import dumps
pacientes = APIRouter()
templates.env.globals['edad_paciente'] = edadPaciente

@pacientes.get('/')
async def listPacientes(request: Request, user=Depends(manager), db : Session = Depends(get_db)):
    controlAcceso(user=user, typeRequired='1.1')
    pacientes = db.query(Pacientes).all()
    estCiviles = db.query(EstadosCiviles).all()
    return templates.TemplateResponse('pacientes.html', context={'request': request, 'pacientes': pacientes,'estCiviles': estCiviles , 'userInfo': user})


@pacientes.get('/ver/{idPaciente}')
async def listPacientes(request: Request, idPaciente:int,  user=Depends(manager), db : Session = Depends(get_db)):
    controlAcceso(user=user, typeRequired='1.1')
    paciente = db.query(Pacientes).filter(Pacientes.id_paciente==idPaciente).first()
    estCiviles = db.query(EstadosCiviles).all()
    return templates.TemplateResponse('paciente.html', context={'request': request, 'paciente': paciente, 'estCiviles': estCiviles, 'userInfo': user})
@pacientes.get('/ver/{idPaciente}/ficha')
async def fichaPaciente(request: Request, idPaciente:int,  user=Depends(manager), db : Session = Depends(get_db)):
    controlAcceso(user=user, typeRequired='1.1')
    preguntas = db.query(Preguntas).all()
    enfermedades = db.query(Enfermedades).all()
    causas_perdidas = db.query(CausasPerdidas).all()
    elementos_higiene = db.query(ElementosHigiene).all()
    paciente = db.query(Pacientes).filter(Pacientes.id_paciente==idPaciente).first()
    cuasasFaltaTrato = db.query(CausasFaltaTrato).all()
    return templates.TemplateResponse('ficha.html', context={'request': request, 'paciente': paciente, 'preguntas': preguntas, 'enfermedades': enfermedades, 'causasPerdidas': causas_perdidas, 'elementosHigiene': elementos_higiene, 'cuasasFaltaTrato': cuasasFaltaTrato ,'userInfo': user})

@pacientes.get('/ficha/{idPaciente}')
async def getFicha(request: Request, idPaciente:int,  user=Depends(manager), db : Session = Depends(get_db)):
    controlAcceso(user=user, typeRequired='1.1')
    ficha = db.query(Fichas).filter(Fichas.id_paciente == idPaciente).first()
    if ficha == None:
        return None
    enfermedades = db.query(EnfermedadesPaciente).filter(EnfermedadesPaciente.id_paciente == idPaciente).all()
    respuestas = db.query(Respuestas).filter(Respuestas.id_paciente == idPaciente).all()
    causasPerdidas = db.query(CausasPerdidasPaciente).filter(CausasPerdidasPaciente.id_paciente == idPaciente).all()
    causasFaltaTrato = db.query(CausasFaltaTratoPaciente).filter(CausasFaltaTratoPaciente.id_paciente == idPaciente).all()
    elementosHigiene = db.query(ElementosHigienePaciente).filter(ElementosHigienePaciente.id_paciente == idPaciente).all()
    
    ficha = ficha.__dict__
    ficha['enfermedades'] = enfermedades
    ficha['respuestas'] = respuestas
    ficha['causasPerdidas'] = causasPerdidas
    ficha['causasFaltaTrato'] = causasFaltaTrato
    ficha['elementosHigiene'] = elementosHigiene
    return ficha

from typing import List, Dict
def crear_lista_dict(datos_list: List, id_paciente: int, campo_id_dict: str, campo_id_tabla: str) -> List[Dict]:
    lista_dict = []
    for i in datos_list:
        lista_dict.append({
            campo_id_tabla: getattr(i, campo_id_dict),
            "id_paciente": id_paciente
        })
    return lista_dict

@pacientes.post('/ficha/{idPaciente}')
async def setFicha(request: Request, idPaciente:int, datos: NewFicha,  user=Depends(manager), db : Session = Depends(get_db)):
    controlAcceso(user=user, typeRequired='1.1')
    fichaPaciente = db.query(Fichas).filter(Fichas.id_paciente == idPaciente)
    
    #Elimino todas las respuestas, enfermedades, etc. del paciente para cargar las actualizadas
    db.query(Respuestas).filter(Respuestas.id_paciente == idPaciente).delete()
    db.query(EnfermedadesPaciente).filter(EnfermedadesPaciente.id_paciente == idPaciente).delete()
    db.query(CausasPerdidasPaciente).filter(CausasPerdidasPaciente.id_paciente == idPaciente).delete()
    db.query(ElementosHigienePaciente).filter(ElementosHigienePaciente.id_paciente == idPaciente).delete()
    db.query(CausasFaltaTratoPaciente).filter(CausasFaltaTratoPaciente.id_paciente == idPaciente).delete()
    db.flush()
    #datos de la nueba ficha
    newFicha = {
        "id_paciente": idPaciente,
        "fecha_act": datetime.now().strftime("%Y-%m-%d"),
        "embarazo": datos.embarazo,
        "tiempo_embarazo": datos.tiempoEmbarazo,
        "tol_anestesia": datos.toleranciaAnestesia,
        "test_elisa": datos.testElisa,
        "ult_consulta": datos.ultimaConsulta,
        "cepillado": datos.cepillado,
        "otro_elemento": datos.elementosHigiene.otroElemento,
        "otro_enfermedad": datos.enfermedades.otraEnfermedad,
        "otro_falta_trato": datos.causasFaltaTrato.otraCausa,
        "comentarios": datos.comentarios
    }
    respuestas = []
    for i in datos.respuestas:
        respuestas.append({
            "id_pregunta": i.idPregunta,
            "id_paciente": idPaciente,
            "bol_respuesta": i.boolRespuesta,
            "text_respuesta": i.textRespuesta
        })
    enfermedades = crear_lista_dict(datos.enfermedades.enfermedades, idPaciente, "idEnfermedad",  "id_enfermedad")
    print(enfermedades)
    causasPerdidas = crear_lista_dict(datos.causasPerdida, idPaciente, 'idCausa', 'id_causa')
    causasFaltaTrato = crear_lista_dict(datos.causasFaltaTrato.causas, idPaciente, 'idCausa', 'id_causa')
    elementosHigiene = crear_lista_dict(datos.elementosHigiene.elementos, idPaciente, 'idElemento', 'id_elemento')
    if fichaPaciente.first() is None:
        new_ficha = Fichas(**newFicha)
        db.add(new_ficha)
        db.flush()
    else:
        fichaPaciente.update(newFicha)
        db.flush()
    newRespuestas = insert(Respuestas).values(respuestas)
    newEnfermedades = insert(EnfermedadesPaciente).values(enfermedades)
    newcausasPerdidas = insert(CausasPerdidasPaciente).values(causasPerdidas)
    newFaltaTrato = insert(CausasFaltaTratoPaciente).values(causasFaltaTrato)
    newElementosHigiene = insert(ElementosHigienePaciente).values(elementosHigiene)
    if respuestas:
        db.execute(newRespuestas)
    if enfermedades:
        db.execute(newEnfermedades)
    if causasPerdidas:
        db.execute(newcausasPerdidas)
    if causasFaltaTrato:
        db.execute(newFaltaTrato)
    if elementosHigiene:
        db.execute(newElementosHigiene)
    db.flush()
    db.commit()
    return datos

@pacientes.get("/search/")
async def search_items(q:str, user=Depends(manager), db : Session = Depends(get_db)):
    controlAcceso(user=user, typeRequired='1.1')
    listPacientes = db.query(Pacientes).filter(or_(Pacientes.nombre.ilike(f"%{q}%"), Pacientes.apellido.ilike(f"%{q}%"), Pacientes.documento.ilike(f"%{q}%"))).all()
    #pacientes = {'Pacientes': listPacientes}
    return listPacientes

@pacientes.get('/info/{idPaciente}')
async def detallePaciente(response:Response, idPaciente:int, user=Depends(manager), db : Session = Depends(get_db)):
    paciente = db.query(Pacientes).filter(Pacientes.id_paciente == idPaciente).first()
    return paciente

@pacientes.post('/nuevo')
async def nuevoPaciente(response: Response, datos: NuevoPaciente, user=Depends(manager), db : Session = Depends(get_db)):
    controlAcceso(user=user, typeRequired='1.1')
    try:
        newPaciente = Pacientes(documento = datos.documento,
                                nombre = datos.nombre,
                                apellido = datos.apellido,
                                nacimiento=datos.nacimiento,
                                sexo = datos.sexo,
                                id_ec = datos.estadoCivil,
                                celular = datos.celular,
                                email = datos.email,
                                direccion = datos.direccion)
        db.add(newPaciente)
        db.commit()
        db.refresh(newPaciente)
        response.status_code = status.HTTP_201_CREATED
        return newPaciente
    except exc.IntegrityError as e:
        response.status_code = status.HTTP_409_CONFLICT
        return "El paciente con documento " + str(datos.documento) + " ya se encuentra registrado"
    
@pacientes.put('/editar/{idPaciente}')
async def editarPaciente(response: Response, idPaciente: int, datos: NuevoPaciente, user=Depends(manager), db : Session = Depends(get_db)):
    try:
        paciente = db.query(Pacientes).filter(Pacientes.id_paciente == idPaciente).first()
        paciente.documento = datos.documento
        paciente.nombre = datos.nombre
        paciente.apellido = datos.apellido
        paciente.nacimiento = datos.nacimiento
        paciente.sexo = datos.sexo
        paciente.id_ec = datos.estadoCivil
        paciente.celular = datos.celular
        paciente.email = datos.email
        paciente.direccion = datos.direccion
        db.commit()
    except exc.IntegrityError as e:
        response.status_code = status.HTTP_409_CONFLICT
        return "Ya existe un paciente con documento " + str(datos.documento) + " registrado en el sistema"
    
@pacientes.delete('/eliminar/{idPaciente}')
async def eliminarPaciente(response: Response, idPaciente: int, user=Depends(manager), db : Session = Depends(get_db)):
    try:
        paciente = db.query(Pacientes).filter(Pacientes.id_paciente == idPaciente).first()
        citas = db.query(Citas).filter(Citas.id_paciente == idPaciente).all()
        for i in citas:
            db.delete(i)
            db.flush()
        db.delete(paciente)
        db.commit()
        return 'Success'
    except exc.IntegrityError as e:
        response.status_code = status.HTTP_409_CONFLICT
        return "No se puede eliminar el paciente"
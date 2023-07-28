from typing import Optional
from pydantic import BaseModel
from datetime import date, time
from typing import List

class Respuestas(BaseModel):
    idPregunta : int
    boolRespuesta : bool
    textRespuesta : Optional[str]

class EnfermedadesPaciente(BaseModel):
    idEnfermedad: int

class Enfermedades(BaseModel):
    enfermedades: Optional[List[EnfermedadesPaciente]]
    otraEnfermedad: Optional[str]

class CausasPerdidaDiente(BaseModel):
    idCausa: int

class CausasFaltaTratoPaciente(BaseModel):
    idCausa: int

class CausasFaltaTrato(BaseModel):
    causas: Optional[List[CausasFaltaTratoPaciente]]
    otraCausa: Optional[str]

class ElementosHigienePaciente(BaseModel):
    idElemento: int

class ElementosHigiene(BaseModel):
    elementos: Optional[List[ElementosHigienePaciente]]
    otroElemento: Optional[str]

class NewFicha(BaseModel):
    embarazo : Optional[int]
    tiempoEmbarazo : Optional[str]
    toleranciaAnestesia : Optional[int]
    testElisa : Optional[int]
    tiempoTestElisa : Optional[str]
    ultimaConsulta : Optional[int] #en meses
    cepillado : Optional[int]
    respuestas: Optional[List[Respuestas]]
    enfermedades : Optional[Enfermedades]
    causasPerdida: Optional[List[CausasPerdidaDiente]]
    causasFaltaTrato : Optional[CausasFaltaTrato]
    elementosHigiene: Optional[ElementosHigiene]
    comentarios: Optional[str]

class FichaPaciente(NewFicha):
    idPaciente: int   

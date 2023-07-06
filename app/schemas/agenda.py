from typing import Optional
from pydantic import BaseModel
from datetime import date, time
from typing import List

class NewCita(BaseModel):
    idPaciente: int
    idDoctor: int
    fecha: date
    hora: time
    duracion : int

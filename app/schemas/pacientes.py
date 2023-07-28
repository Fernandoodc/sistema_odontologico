from typing import Optional
from pydantic import BaseModel
from datetime import date, time
from typing import List

class NuevoPaciente(BaseModel):
    documento: int
    nombre: str
    apellido: str
    nacimiento: date
    sexo: bool #true = mas ; false = fem
    estadoCivil: int
    celular: str
    email: str
    direccion: str
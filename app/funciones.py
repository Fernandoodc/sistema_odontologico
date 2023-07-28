from datetime import datetime
from database.conexion import SessionLocal
from database.models import Pacientes
def edadPaciente(idPaciente):
    session = SessionLocal()
    paciente = session.query(Pacientes).filter(Pacientes.id_paciente==idPaciente).first()
    now = datetime.now()
    nacimiento = paciente.nacimiento
    #edad = int((now - datetime.strptime(str(nacimiento), '%Y-%m-%d')).days / 365)
    edad = now.year - nacimiento.year - ((now.month, now.day) < (nacimiento.month, nacimiento.day))
    return str(edad) + " años"

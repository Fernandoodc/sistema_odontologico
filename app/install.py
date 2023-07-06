from database.conexion import SessionLocal, engine
from database.models import User, Permisos, Doctores, Especialidades, TiposUsuarios
from database import models

models.Base.metadata.create_all(bind=engine)
print('Instalación del Odontologico\t')
opc = (input('Poner en condiciones la BD? (y/n) '))
if opc == 'y' or opc == 'Y':
    session = SessionLocal()
    permisos = ['1.1', '2.1' , '3.1', '3.2', '3.3', '4.1', '4.2', '5.1']
    tiposUser = [
        {
            'id': 1,
            'descripcion': 'Usuario'
        }
        ,{
            'id': 2,
            'descripcion': 'Doctor'
        }
    ]
    for i in tiposUser:
        newTipUser = TiposUsuarios(
            id_tipo = i['id'],
            descripcion = i['descripcion']
        )
        session.add(newTipUser)
        session.flush()
    print('Creando Usuario Administrador...')
    admin = User(username = 'admin',
                    password = 'pbkdf2:sha256:260000$sduFXVnyhVVnGRkt$593abe631223f0fa78fcbab6341d44f60aca9bd50adfe110c07825f415a0ae9c', 
                    nombre = 'admin', 
                    apellido = 'admin',
                    documento = '123',
                    activo = True,
                    id_tipo = 2
                )
                
    session.add(admin)
    session.flush()
    session.refresh(admin)
    especialidad = Especialidades(descripcion = "Odontología general")
    session.add(especialidad)
    session.flush()
    session.refresh(especialidad)
    doctor = Doctores(
        id_usuario = admin.id,
        id_especialidad = especialidad.id_especialidad,
        registro = '123'
    )
    session.add(doctor)
    session.flush()
    print('Agregando Permisos...')
    for i in permisos:
        permiso = Permisos(id_usuario = admin.id, codigo = i)
        session.add(permiso)
    session.flush()
    session.commit()
    session.close()
    print('Base de Datos configurada')
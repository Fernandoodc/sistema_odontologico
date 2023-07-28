from database.conexion import SessionLocal, engine
from database.models import User, Permisos, Doctores, Especialidades, TiposUsuarios, EstadosCiviles, Enfermedades, Preguntas, CausasPerdidas, ElementosHigiene, CausasFaltaTrato
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
        registro = '123',
        intervalo = 30
    )
    session.add(doctor)
    session.flush()
    print('Agregando Permisos...')
    for i in permisos:
        permiso = Permisos(id_usuario = admin.id, codigo = i)
        session.add(permiso)
    session.flush()
    print('Agregando Estados civiles')
    estCiviles = ['Soltero/a', 'Casado/a', 'Separado/a', 'Divorciado/a', 'Viudo/a']
    for i in estCiviles:
        newEc = EstadosCiviles(descripcion = i)
        session.add(newEc)
        session.flush

    enfermedades = ['Tuberculosis', 'Enf. de Chagas', 'Ulceras', 'Disturbios psiquicos', 'Lepra', 'Fiebre Reumática', 'Enf. Cardiacas', 'Convulciones', 'Hepatitis', 'Sinusitis', 'Hipert. Arterial', 'Probl. de Coagul.', 'Malaria', 'Alergia', 'Anemia', 'Diabetes', 'S.I.D.A.', 'Lesión del Higado', 'Hemofilia']
    for i in enfermedades:
        newEnfermedad = Enfermedades(descripcion = i)
        session.add(newEnfermedad)
        session.flush()
    causas_perdidas = ['Caries', 'Accidentes', 'Movilidad']
    for i in causas_perdidas:
        newCausa = CausasPerdidas(descripcion = i)
        session.add(newCausa)
        session.flush()
    preguntas = [
        {
            'pregunta': '¿Está siendo sometido a algún tratamiento médico actualmente?',
            'sub_pregunta': '¿Hace cuanto tiempo?'
        },
        {
            'pregunta': '¿Está haciendo uso de algún medicamento?',
            'sub_pregunta': '¿Cual es?'
        },
        {
            'pregunta': '¿Necesitó o necesita periódicamente de transfución sanguínea o derivados',
            'sub_pregunta': 'Motivo'
        },
        {
            'pregunta': '¿Fue sometido a alguna sirugía?',
            'sub_pregunta': '¿Cual?'
        },
        {
            'pregunta': '¿Sangra mucho despues de una extración o corte?',
            'sub_pregunta': None
        },
        {
            'pregunta': '¿Fuma?',
            'sub_pregunta': '¿Hace cuanto Tiempo?, Cantidad'
        },
        {
            'pregunta': '¿Toma bebidas alcohólicas?',
            'sub_pregunta': '¿Hace cuanto Tiempo?, Cantidad'
        },
    ]

    for i in preguntas:
        newPregunta = Preguntas(pregunta = i['pregunta'], sub_pregunta = i['sub_pregunta'])
        session.add(newPregunta)
        session.flush()
    elementos_higiene = ['Cepillo', 'Hilo dental', 'Enjuague']
    for i in elementos_higiene:
        newElemento = ElementosHigiene(descripcion = i)
        session.add(newElemento)
        session.flush()

    causasFaltaTraro = ['Falta de tiempo', 'Problemas económicos', 'Desinterés']
    for i in causasFaltaTraro:
        newCausa = CausasFaltaTrato(descripcion = i)
        session.add(newCausa)
        session.flush()
    session.commit()
    session.close()
    print('Base de Datos configurada')
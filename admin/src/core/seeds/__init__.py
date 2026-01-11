from src.core.models.users import User
from src.core.config.database import db
from src.core import auth
from src.core.models.permissions import Permission, permissions
from src.core.models.roles import Role, RoleEnum
from src.core.models.institutions import Institution
from src.core.models.user_institution_role import UserInstitutionRole
from src.core.models.solicitude import Solicitude
from src.core.models.note import Note
from src.core.models.Institutional_Services.services import Service
from datetime import datetime
from src.core.config.database import db
import random
from src.core.models.solicitude import Status, TypeService
from datetime import timedelta

    
list_Names = ["Servicio1","Servicio2","Servicio3","Servicio4","Servicio5","Servicio6",
              "Servicio1","Servicio1","Servicio4","Servicio10"]
    
list_Desp = ["Descripción del servicio1","Descripción del servicio2","Descripción del servicio3",
                "Descripción del servicio4","Descripción del servicio5","Descripción del servicio6",
                "Descripción del servicio","Descripción del servicio1","Descripción del servicio4",
                "Descripción del servicio10"]

list_kEY = [["UNO","I"],
                ["DOS","II"],
                ["TRES","III"],
                ["CUATRO","IV"],
                ["CINCO","V"],
                ["SEIS","VI"],
                ["SIETE","VII"],
                ["OCHO","VIII"],
                ["NUEVE","IX"],
                ["DIES","X"]]

list_centers = [["Centros1","Centros11"],["Centros2","Centros13"],["Centros3","Centros12"],
                ["Centros4","Centros16"],["Centros5","Centros19"],["Centros6","Centros20"],
              ["Centros1","Centros17"],["Centros1","Centros18"],["Centros4","Centros21"],
              ["Centros10","Centros23"]]

def create_solicitude(**kwargs):
    solicitude = Solicitude(**kwargs)
    db.session.add(solicitude)
    db.session.commit()
    return solicitude

def create_Service(nam,des,key,cent,inst):
     
    new_service = Service(
    name=nam,
    description=des,
    search_keywords=key,
    authorized_centers = cent,
    type_of_service=random.choice([Service.TypeService.Análisis, Service.TypeService.Consultoría, Service.TypeService.Desarrollo]),  # Otra opción: Service.TypeService.Consultoría
    enabled=random.choice([True, False]),
    updated_at=datetime.utcnow(),
    inserted_at=datetime.utcnow(),
    institutions_id=inst
    )
    
    return new_service

        
def create_user_institution_role(**kwargs):
    user_institution_role = UserInstitutionRole(**kwargs)
    db.session.add(user_institution_role)
    db.session.commit()
    return user_institution_role

def update_user_active(**kwargs):
    user = kwargs['usub']
    user.active = kwargs['active']
    db.session.commit()

def update_user_institution_role(**kwargs):
    userInstitutionRole = kwargs['usubRol']
    userInstitutionRole.role_id = kwargs['rol']
    db.session.commit()

def assign_roles(permission, roles):
    permission.roles.extend(roles)
    db.session.add(permission)
    db.session.commit()
    return permission

def assign_permissions(role, permissions):
    role.permissions.extend(permissions)
    db.session.add(role)
    db.session.commit()
    return role

def create_permits(*args):
    for permission in args:
        db.session.add(permission)
    db.session.commit()

def create_roles(*args):
    for role in args:
        db.session.add(role)
    db.session.commit()

def create_institutions(**kwargs):
    institution = Institution(**kwargs)
    db.session.add(institution)
    db.session.commit()
    return institution

def create_note(**kwargs):
    note = Note(**kwargs)
    db.session.add(note)
    db.session.commit()
    return note

def run():
    permission_index = Permission(name='user_index')
    permission_new = Permission(name='user_new')
    permission_destroy = Permission(name='user_destroy')
    permission_update = Permission(name='user_update')
    permission_show = Permission(name='user_show')

    # Para SERVICE
    permission_service_index = Permission(name='service_index')
    permission_service_new = Permission(name='service_new')
    permission_service_destroy = Permission(name='service_destroy')
    permission_service_update = Permission(name='service_update')
    permission_service_show = Permission(name='service_show')

    # Para INSTITUTION
    permission_institution_index = Permission(name='institution_index')
    permission_institution_new = Permission(name='institution_new')
    permission_institution_destroy = Permission(name='institution_destroy')
    permission_institution_update = Permission(name='institution_update')
    permission_institution_show = Permission(name='institution_show')

    # Para Configuracion
    permission_configuracion_show = Permission(name='config_show')
    permission_configuracion_update = Permission(name='config_update')

    
    create_permits(
        permission_index, permission_new, permission_destroy, permission_update, permission_show,
        permission_service_index, permission_service_new, permission_service_destroy, permission_service_update, permission_service_show,
        permission_institution_index, permission_institution_new, permission_institution_destroy, permission_institution_update, permission_institution_show
    )

    #Creo los roles
    role_super_admin = Role(name=RoleEnum.SUPER_ADMIN)
    role_admin = Role(name=RoleEnum.ADMIN)
    role_operator = Role(name=RoleEnum.OPERATOR)
    role_owner = Role(name=RoleEnum.OWNER)

    create_roles(role_super_admin, role_admin, role_operator, role_owner)

    # Para el rol Dueño/a sobre servicios
    assign_permissions(
        role_owner, 
        [
            permission_service_index, permission_service_show, permission_service_update,
            permission_service_new, permission_service_destroy
        ]
    )

    # Para el rol Dueño/a sobre instituciones
    assign_permissions(
        role_owner, 
        [
            permission_institution_index,
            permission_institution_new,
            permission_institution_destroy,
            permission_institution_update
        ]
    ) 

    # Para el rol Administrador/a
    assign_permissions(
        role_admin, 
        [
            permission_service_index, permission_service_show, permission_service_update,
            permission_service_new, permission_service_destroy
        ]
    )

    # Para el rol Operador/a
    assign_permissions(
        role_operator, 
        [
            permission_service_index, permission_service_show, permission_service_update,
            permission_service_new
        ]
    )

    
    assign_permissions(
        role_super_admin, 
        [
            permission_index, permission_new, permission_destroy, permission_update, permission_show,
            permission_service_index, permission_service_new, permission_service_destroy, permission_service_update, permission_service_show,
            permission_institution_index, permission_institution_new, permission_institution_destroy, permission_institution_update, permission_institution_show,
            permission_configuracion_update, permission_configuracion_show
        ]
    )
    
    assign_permissions(role_admin, [permission_index, permission_new, permission_destroy, permission_update, permission_show])
    assign_permissions(role_operator, [permission_index, permission_new, permission_update, permission_show])
    assign_permissions(role_owner, [permission_index, permission_new, permission_destroy, permission_update, permission_show])

    institution1 = create_institutions(name="Institucion 1", active=True, address="Calle 1", contact_info="123456789", location="-34.9206,-57.9538" , web="www.institucion1.com", key_words="Institucion 1", work_schedule="Lunes a Viernes de 8am a 5pm")
    institution2 = create_institutions(name="Institucion 2", active=True, address="Calle 2", contact_info="123456789", location="-34.9206,-57.9538", web="www.institucion2.com", key_words="Institucion 2", work_schedule="Lunes a Viernes de 8am a 5pm")
    institution3 = create_institutions(name="Institucion 3", active=True, address="Calle 2", contact_info="123456789", location="-34.9206,-57.9538", web="www.institucion3.com", key_words="Institucion 3", work_schedule="Lunes a Viernes de 8am a 5pm")
    institution4 = create_institutions(name="Institucion 4", active=True, address="Calle 2", contact_info="123456789", location="-34.9206,-57.9538", web="www.institucion4.com", key_words="Institucion 4", work_schedule="Lunes a Viernes de 8am a 5pm")
    ins5 = create_institutions(name="Colores navideños", active=True, address="Calle 2 entre av. 61 y 62", contact_info="+54 3342 121 42 4244", location="-34.9206,-57.9538", web="https://www.linkedin.com/in/valentin-dom%C3%A9", key_words="Institucion 4", work_schedule="Lunes a Viernes de 8am a 5pm")


    user = auth.create_user(email= "boca@gmail.com", password = "123", name="Román", last_name="Riquelme")
    user1 = auth.create_user(email= "campeon@gmail.com", password = "123", name="Edison", last_name="Cavani")
    user2 = auth.create_user(email= "el_crack_de_facu@gmail.com", password = "123", name="Facu", last_name="Crack")
    u3 = auth.create_user(email= "pan_dulce@gmail.com", password = "123", name="Santa Nicolas", last_name="Claus")

    create_user_institution_role(user_id=user.id, institution_id=institution1.id, role_id=role_super_admin.id)
    create_user_institution_role(user_id=user1.id, institution_id=institution2.id, role_id=role_admin.id)
    create_user_institution_role(user_id=user1.id, institution_id=institution1.id, role_id=role_owner.id)
    create_user_institution_role(user_id=user2.id, institution_id=institution1.id, role_id=role_operator.id)

    create_user_institution_role(user_id=u3.id, institution_id=ins5.id, role_id=role_owner.id)
    
    list_inst = [institution1.id,institution2.id,institution4.id,institution3.id]
    list_services = []
    for numero in range(10):
        new_service = create_Service(list_Names[numero],list_Desp[numero],list_kEY[numero],list_centers[numero],random.sample(list_inst,1)[0])
        list_services.append(new_service)
        # Agregar el nuevo servicio a la base de datos
        db.session.add(new_service)
        db.session.commit()
      
      
    new_service = Service(
    name="Fabricición de colores",
    description="Unicos",
    search_keywords="A  B  C ",
    authorized_centers = "Centro en La Plata",
    type_of_service=Service.TypeService.Análisis,  # Otra opción: Service.TypeService.Consultoría
    enabled= True,
    updated_at=datetime.utcnow(),
    inserted_at=datetime.utcnow(),
    institutions_id=ins5.id
    )
    db.session.add(new_service)
    db.session.commit()
    
    # Crea 10 solicitudes a institución con un comentario cada una
    for numero in range(20):
        solicitud_creada = create_solicitude(user_id=random.randint(1,3),
                                            service_id= new_service.id,
                                            status=random.choice([Status.ACEPTED, Status.REJECTED, Status.IN_PROCESS, Status.FINISHED, Status.CANCELED]),
                                            type_of_service=random.choice([TypeService.Análisis, TypeService.Consultoría, TypeService.Desarrollo]))
        
        create_note(user_id = solicitud_creada.user_id,
                    solicitude_id = solicitud_creada.id,
                    content = " - Primer nota.",
        )


    # Crea 10 solicitudes
    for numero in range(10):
        create_solicitude(user_id=random.randint(1,3),
                        service_id=list_services[numero].id,
                        status=random.choice([Status.ACEPTED, Status.REJECTED, Status.IN_PROCESS, Status.FINISHED, Status.CANCELED]),
                        type_of_service=random.choice([TypeService.Análisis, TypeService.Consultoría, TypeService.Desarrollo]))
        
    # Crea 300 solicitudes adicionales
    for i in range(300):
        user_id = random.randint(1, 3)
        service_id = random.choice(list_services).id
        comment = "Descripción de la solicitud"
        status = random.choice([Status.ACEPTED, Status.REJECTED, Status.IN_PROCESS, Status.FINISHED, Status.CANCELED])
        type_of_service = random.choice([TypeService.Análisis, TypeService.Consultoría, TypeService.Desarrollo])
        
        solicitude = create_solicitude(user_id=user_id,
                                    service_id=service_id, 
                                    status=status,
                                    type_of_service=type_of_service)
        
        # Modifica 100 solicitudes para establecer el estado como "FINISHED" y variar la fecha de actualización
        if i < 100:
            solicitude.status = Status.FINISHED
            # Variar la fecha de actualización entre 3 y 50 días después de la fecha de creación
            update_date = solicitude.inserted_at + timedelta(days=random.randint(3, 50))
            solicitude.updated_at = update_date
        else:
            update_date = solicitude.inserted_at + timedelta(days=random.randint(20, 50))
            solicitude.updated_at = update_date

        db.session.commit()

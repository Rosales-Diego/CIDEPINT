from src.core.config.database import db
from src.core.models.confirmation_user import ConfirmationUser
from src.core.models.users import User
from src.core.models.Institutional_Services.services import Service as Ser
from src.core.models.solicitude import Solicitude
from src.core.models.institutions import Institution
from src.core.models.Institutional_Services.services import Service
from src.core.models.user_institution_role import UserInstitutionRole
from src.core.models.note import Note
from src.core.bcrypt import bcrypt
from src.core.seeds import create_user_institution_role

#-------------------------------------------------------------------------------------------
#Model Note
def get_me_notes_for_service(solicitud_id, user_id):
    notes = (
        db.session.query(Note)
        .join(Solicitude)
        .join(Service, Service.id == Solicitude.service_id)
        .filter(User.id == user_id, Solicitude.id == solicitud_id)
        .all()
    )
    
    return notes

def get_me_notes(user_id):
    # Obtén las notas y carga la relación con el servicio
    return Note.query.filter_by(user_id=user_id)

def get_notes_service(service_id):
    notes = (
        db.session.query(Note)
        .join(Solicitude)
        .join(Service, Service.id == Solicitude.service_id)
        .filter(Service.id == 11)
        .all()
    )
    
    return notes

def get_names_services(notes):
    lista= []
        
    for nota in notes:
        solicitud  = Solicitude.query.filter_by(id=nota.solicitude_id).first()
        id_service = solicitud.service_id
        service = Service.query.filter_by(id=id_service).first()
        name_institution = Institution.query.filter_by(id =service.institutions_id ).first().name
                    
        # Agregar el nombre de la institución a la lista
        lista.append({
                'service_name': service.name,
                'institution_name': name_institution,
                'user_id' : nota.user_id,
                'service_id' : service.id,
                'id' :solicitud.id,
                'status': solicitud.status,
                'type_of_service':solicitud.type_of_service,
                'inserted_at' :solicitud.inserted_at,
                'content': nota.content,
                
        })    
        
    return lista
#-------------------------------------------------------------------------------------------
# Model User
def update_user_with_form(user, form):
    user.email = form.email.data
    user.name = form.name.data
    user.last_name = form.last_name.data
    user.active = form.active.data == 'activo'

    db.session.commit()

def delete_user(user):

    # Obtén el usuario que deseas eliminar por su ID
    user_id_to_delete = user.id 
    
    if "super_admin" in [role.name.value for role in user.roles]:
        # No permitas la eliminación de super administradores
        print("No se puede eliminar un super_admin.")
        return False

    if user:
        # Antes de eliminar el usuario, primero elimina las relaciones en UserInstitutionRole
        user_institution_roles = UserInstitutionRole.query.filter_by(user_id=user_id_to_delete).all()
       
        for user_institution_role in user_institution_roles:
           
            db.session.delete(user_institution_role)
            db.session.commit()

        # Elimina el usuario
        db.session.delete(user)
        db.session.commit()
        return True
    else:
        return False
        

def find_user_by_id(id):
    result = User.query.get(id)
    return result

def find_user_by_email(email):
    result = User.query.filter_by(email = email).first()
    return result


def exist_mail(mail):
    existing_user = User.query.filter_by(email=mail).first()
    if existing_user:
        return True
    return False

def list_permissions_by_user_id(id):
    user = find_user_by_id(id)
    
    if user is None:
        return None

    # Ahora, recorre las relaciones para obtener los permisos asociados al usuario
    permissions = []

    for role in user.roles:
        permissions.extend(role.permissions)

    # Elimina duplicados si es necesario
    permissions = list(set(permissions))

    # Convierte los permisos a un formato que quieras
    permission_data = [ p.name for p in permissions]

    #permission_data =  [ p.name for p in permission_data]
    
    return permission_data

def list_confirmation():
	issues = ConfirmationUser.query.all()
	return issues

def list_users():
	issues = User.query.all()
	return issues

def create_user(**kwargs):

    hash = bcrypt.generate_password_hash(kwargs["password"].encode("utf-8"))
    kwargs.update(password=hash.decode("utf-8"))
    user = User(**kwargs)
    db.session.add(user)
    create_user_institution_role(user_id=user.id,role_id=3)
    db.session.commit()
    return user

def create_confirmation(**kwargs):
	confir = ConfirmationUser(**kwargs)
	db.session.add(confir)
	db.session.commit()
	return confir

def create_user_with_form(form):
    nuevo = create_user(email=form.email.data,password=form.password.data,
                        name=form.name.data, last_name=form.last_name.data)
    
    nuevo.active =(form.active.data == 'activo')
    
    db.session.add(nuevo)
    db.session.commit()

    
# Model Instituciosne
"""------------------------------------------------------------------"""

def list_intitucions():
    institutions = Institution.query.all()
    return institutions
    
def validate_location(value):
    lat, lon = map(float, value.split(','))
    try:
        # Verificar el formato y convertir a flotantes
        lat, lon = map(float, value.split(','))
        
        # Verificar los rangos de latitud y longitud
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            raise ValueError("Latitud y longitud fuera de rango")
        
        return value
    except ValueError:
        raise ValueError("Ubicación no válida. Debe seguir el formato 'latitud, longitud'")
        
"""------------------------------------------------------------------"""
# Model Services
"""------------------------------------------------------------------"""
def list_service(institution_id):
    service = Ser.query.filter_by(institutions_id=institution_id).all()
    return service

def get_request_to(service_id):
    services = Solicitude.query.filter_by(service_id=service_id)
    res = []
    res.extend(services)
    return res

def get_service(service_id):
    service = Ser.query.get(service_id)
    return  service

def  create_service(**kwargs):  
    
    # Obtener el valor de 'enabled' de kwargs y convertirlo a un booleano
    enabled = kwargs.get('enabled', False)  # Establecer el valor predeterminado como False si 'enabled' no está presente
    
    # Convertir 'enabled' a un booleano
    enabled = enabled.lower() == 'true' if isinstance(enabled, str) else bool(enabled)
    
    # Actualizar kwargs con el valor booleano
    kwargs['enabled'] = enabled
    
    service = Ser(**kwargs)

    db.session.add(service)
    db.session.commit()
    
    return service

"""------------------------------------------------------------------"""
# Model Solicitude
#----------------------------------------------------------------------

def list_solicitude():
    solicitude = Solicitude.query.all()
    return solicitude

def get_me_requests(user_id):
    my_requests = Solicitude.query.filter_by(user_id = user_id)
    result = []
    result.extend(my_requests)
    
    my_requests = (
        db.session.query(
            Solicitude.id,
            Solicitude.service_id,
            Solicitude.user_id,
            Solicitude.status,
            Solicitude.type_of_service,
            Solicitude.updated_at,
            Solicitude.inserted_at,
            Service.name.label("service_name")  # Agregamos el nombre del servicio como un alias
        )
        .join(Service, Solicitude.service_id == Service.id)  # Hacemos un join con la tabla Service
        .filter(Solicitude.user_id == user_id)
        .all()
    )

    result = []
    for request_data in my_requests:
        request_dict = {
            "id": request_data.id,
            "service_id": request_data.service_id,
            "user_id": request_data.user_id,
            "status": request_data.status,
            "type_of_service": request_data.type_of_service,
            "updated_at": request_data.updated_at,
            "inserted_at": request_data.inserted_at,
            "service_name": request_data.service_name  # Agregamos el nombre del servicio al resultado
        }
        result.append(request_dict)

    return result


# Model Institutions
#------------------------------------------------------------------------

def obtener_instituciones_por_ids(ids_instituciones):
    # Consulta las instituciones cuyos IDs están en la lista ids_instituciones
    instituciones = Institution.query.filter(Institution.id.in_(ids_instituciones)).all()

    return instituciones

def get_service_for_institution(id):
    services = Ser.query.filter_by(institutions_id = id)
    list = []
    for i in services:
        list.append(i)
    return list

def delete_institution(institucion):
    institucion.users.clear()
    db.session.delete(institucion)
    db.session.commit()

def update_institution():
    db.session.commit()

def get_institutions():
    institutions = Institution.query.all()
    return institutions


def find_institution_by_name(name): 
    result = Institution.query.get(1)
    return result

def find_institution_by_id(id):
    result = Institution.query.get(id)
    return result

def  create_institution(**kwargs):  
    """
    # Obtener el valor de 'enabled' de kwargs y convertirlo a un booleano
    enabled = kwargs.get('enabled', False)  # Establecer el valor predeterminado como False si 'enabled' no está presente
    
    # Convertir 'enabled' a un booleano
    enabled = enabled.lower() == 'true' if isinstance(enabled, str) else bool(enabled)
    
    # Actualizar kwargs con el valor booleano
    kwargs['enabled'] = enabled
    """
    
    institution = Institution(**kwargs)

    db.session.add(institution)
    db.session.commit()
    
    return institution

"""--------------------------------------------------------------------------------------------------"""
def check_user_role(user_id):
    # Query the database to find the UserInstitutionRole entry for the given user_id
    user_role = UserInstitutionRole.query.filter_by(user_id=user_id).first()

    # Check if the user_role exists and has role_id equal to 1
    if user_role and user_role.role_id == 1:
        return True
    else:
        return False
    
    
def get_user_institutions(user_id):
    # Query the database to find all UserInstitutionRole entries for the given user_id
    user_institutions = UserInstitutionRole.query.filter_by(user_id=user_id).all()

    # Extract institution IDs from the query results
    institution_ids = [user_institution.institution_id for user_institution in user_institutions]

    return institution_ids


#----------------------------------------------------------------------------------------------------

def get_notes_Solicitud(solicitud_id):
    
    # Obtén la instancia de la solicitud
    solicitud = Solicitude.query.get(solicitud_id)

    # Verifica si la solicitud existe
    if solicitud:
        # Accede a las notas asociadas a la solicitud a través del atributo 'notes'
        notas_de_solicitud = solicitud.notes
        return(notas_de_solicitud)
    else:
        print(f"No se encontró la solicitud con ID {solicitud_id}")
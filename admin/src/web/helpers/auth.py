from flask import abort
from flask import request
from functools import wraps
from flask import session
from src.core.models import find_user_by_id, find_user_by_email
from src.core.models import list_permissions_by_user_id
from src.core.models import ConfirmationUser, User

def is_valid_confirmation_token(token):
    confir = ConfirmationUser.query.filter_by(token=token).first()
    return confir != None
    
def is_authenticated(session):
    return session.get("user") is not None
 
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #Linea antes de ejecutar la función decorada
        if (not is_authenticated(session)):
            return abort(401)
        #Ejecución de la función decorada
        return f(*args, **kwargs)
    return decorated_function

def has_permission_bool(requiered_permissions_list): 
    has_permission = True


    user = find_user_by_id(session.get("user_id"))
    if user:
        id_user = user.id
    else:
        return False

    user_permissions_list = list_permissions_by_user_id(id_user)

    
    for permission in requiered_permissions_list: 
        if not (permission in user_permissions_list):
            print(f"{permission} no está el permiso ")
            has_permission = False
            break

    return has_permission

def has_permission(requiered_permissions_list): 
    has_permission = True


    user = find_user_by_id(session.get("user_id"))
    if user:
        id_user = user.id
    else:
        return abort(401)

    user_permissions_list = list_permissions_by_user_id(id_user)

    
    for permission in requiered_permissions_list: 
        if not (permission in user_permissions_list):
            print(f"{permission} no está el permiso ")
            has_permission = False
            break

    return has_permission
    

def in_maintenance(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #agregar lógica de validacion
        return f(*args, **kwargs)
    return decorated_function

def is_api_authenticated(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #agregar lógica de validacion
        data = request.headers.get('Authorization')
        if not data or not find_user_by_email(data):
            return abort(401)
        return f(*args, **kwargs)
    return decorated_function

def find_user_by_id(id):
    return User.query.filter_by(id=id).first()
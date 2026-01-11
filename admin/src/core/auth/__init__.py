from src.core.config.database import db
from src.core.models.users import User
from src.core.models import ConfirmationUser

from src.core.bcrypt import bcrypt


def list_users():
    return User.query.all()

def create_user(**kwargs):
    """
    Agrega un usuario al modelo, con la clave hasheada
    """
    hash = bcrypt.generate_password_hash(kwargs["password"].encode("utf-8"))
    kwargs.update(password=hash.decode("utf-8"))
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()
    return user

def find_confirmation_by_email(email):
    return ConfirmationUser.query.filter_by(email=email).first()

def find_user_by_email_and_pass(email):
    return User.query.filter_by(email=email).first()

def check_user(email, password):
    user =  find_user_by_email_and_pass(email)
    #print("Res de busqueda", user)
    if user and bcrypt.check_password_hash(user.password, password.encode("utf-8")):
        return user

    return None

def find_user_by_id(id):
    return User.query.filter_by(id=id).first()


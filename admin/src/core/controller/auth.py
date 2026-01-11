from flask import Blueprint
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask import request
from flask import abort
from flask import session
import random
import string
import os

from src.core import auth
from src.web.helpers.auth import is_authenticated
from src.web.helpers.auth import is_valid_confirmation_token

from src.core.models import ConfirmationUser
from src.core.models import User
from flask_mail import Message

from src.core.models import create_confirmation
from src.core.auth import create_user

from authlib.integrations.flask_client import OAuth
from src.core.config.database import db
from flask import current_app

# Código para generar un token de confirmación
def generate_confirmation_token():
    token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
    return token


auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.get("/")
def login():
    if not is_authenticated(session):
        return render_template("auth/login.html")
    return redirect("/")


@auth_blueprint.post("/authenticate")
def authenticate():
    params = request.form

    user = auth.check_user(params["email"], params["password"])

    if not user:
        flash("Email o clave incorrecta.", "error")
        return redirect(url_for("auth.login"))

    flash("Bienvenido nuevamente.", "succes")

    session['user'] = user
    session['user_id'] = user.id

    return redirect(url_for("home"))


@auth_blueprint.get("/logout")
def logout():
    if session.get("user"):
        del session["user"]
        session.clear()
        flash("La sesión se cerró correctamente.", "info")

    else:
        
        flash("Men, primero tenes que iniciar sesión.", "info")

    return redirect("/")



@auth_blueprint.get("/register")
def register():
    return render_template("auth/register.html")


@auth_blueprint.post("/validate_register")
def validate_register():

    """
    Esta función se encarga de validar el mail y enviarle un mensaje con la URL y token único
    para que termine el registro
    """
    from app import mail
    params = request.form

    email = params["email"]

    user = auth.find_user_by_email_and_pass(email)
    confir = auth.find_confirmation_by_email(email)
    
    if user != None or confir != None:
        #Usuario ya existe
        flash("Lo sentimos, este correo electrónico ya esta registrado. Por Favor si ya te has registrado ve a login", "error")
        return redirect(url_for("auth.register"))

    #Usuario correcto

    # Genera un token de confirmación
    token = generate_confirmation_token()

    confir = create_confirmation(email = email, token = token)

    # Envía el correo electrónico con el token
    msg = Message('Completa tu registro', sender=os.getenv('MAIL_USERNAME'), recipients=[email])
    msg.body = f'¡Hola {email}!\n\nHaz clic en el siguiente enlace para completar tu registro\n\n{url_for("auth.complete_registration", token=token, _external=True)}'
    mail.send(msg)


    flash("Primera etapa exitosa, ahora revisa tu correo electrónico para continuar.", "success")

    # Redirige al usuario a la página principal
    return redirect("/")

@auth_blueprint.route("/complete_registration/<token>", methods=["GET", "POST"])
def complete_registration(token):

    """
    Esta función solo puede ser accedida si previamente se inicio el registro y permite terminar de
    cargar los datos del usuario
    """

    # Verifica si el token es válido
    if is_valid_confirmation_token(token):
        if request.method == "POST":
            # Recupera los datos del formulario de registro (nombre de usuario, contraseña, etc.)
            email = request.form.get("email")
            password = request.form.get("password")
            name = request.form.get("name")
            last_name = request.form.get("last_name")

            # Guarda la información de usuario en la base de datos y asigna el rol correspondiente
            user = create_user(email=email, password=password, name=name, last_name=last_name)
            
            flash("Registro completado. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for("auth.login"))
        else:
            return render_template("auth/complete_registration.html", token=token)
    else:
        flash("El enlace de confirmación es inválido o ha expirado.", "error")
        return redirect(url_for("auth.register"))




'''Configurar la integración de OAuth con Google para la autenticación de usuarios'''

app = current_app
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(app)
oauth.register(
    name='google',
    redirect_uri='http://127.0.0.1:5000/callback',
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    client_id = os.getenv('GOOGLE_CLIENT_ID'),
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@auth_blueprint.route('/register_google')
def register_google():
    return oauth.google.authorize_redirect('http://127.0.0.1:5000/auth/callback')


@auth_blueprint.route('/callback')
def callback():
    from app import mail
    token = oauth.google.authorize_access_token()
    token_user = (token,'')
    info=token_user[0]
    datos=info['userinfo']
    email=datos['email']
    datosDB = User.query.filter_by(email=email).first()
    passw = generate_confirmation_token()
    #passw = '123'
    if not datosDB:
        # Carga el usuario en la DB
        user=auth.create_user(email= email, password = passw, name=datos['given_name'], last_name=datos['family_name'])
        user.active=True
        db.session.add(user)
        db.session.commit()
        # Envía el correo electrónico con la contraseña
        msg = Message('Contraseña CIDEPINT', sender=os.getenv('OAUTH_SENDER'), recipients=[email])
        msg.body = f'¡Hola {email}!\n\nHaz clic en el siguiente enlace para ingresar a nuestra web por primera vez https://grupo24.proyecto2023.linti.unlp.edu.ar/LoginGoogle, su contraseña es {passw}'
        mail.send(msg)
        flash(f"Ha sido registrado. Su password es: {passw}", "success")                
    return redirect('http://localhost:5173/LoginGoogle')

import json
from os import environ, urandom
from flask import Flask, render_template
from src.core.models.roles import Role
from src.core.models.user_institution_role import UserInstitutionRole
from src.core.controller.errors import error_404 as error
from src.core.controller.errors import error_401
from src.web.configs import config
from src.core.config import database
from src.core import seeds
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.core.models.users import User
from src.core.config.database import db
from src.core.auth import check_user


#Importación de blueprints
from src.core.controller.auth import auth_blueprint
from src.core.controller.user import user_blueprint
from src.core.controller.service import service_bluprint
from src.web.api.services import service_api_bp
from src.web.api.auth import auth_api_bp
from src.web.api.institutions import institution_api_bp
from src.web.api.user import user_api_bp
from src.web.api.services_types import services_types_api_bp
from src.web.api.solicitude import solicitude_api_bp
from src.web.api.contact import contact_api_bp
from src.web.api.note import notes_api_bp

from src.core.controller.relation import relation_blueprint
from src.core.controller.configuration import configuration_blueprint
from src.core.controller.institution import institutions_blueprint
from src.core.controller.request import requests_blueprint

from src.web.helpers.auth import is_authenticated
from src.core.controller import auth
from src.core.models.institutions import Institution
from src.core.models import list_intitucions , check_user_role ,get_user_institutions,obtener_instituciones_por_ids
from flask_session import Session
from flask import session
from src.core import bcrypt
from flask_cors import CORS
from src.web.helpers.auth import has_permission_bool

def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    app.secret_key = environ.get("SECRET_KEY") or urandom(24)
    
    # CORS
    CORS(app)

    #JWT
    jwt = JWTManager(app)
    jwt.init_app(app)

    app.config.from_object(config[env])
    Session(app)

    bcrypt.init_app(app)

    # Registro los blueprints
    app.register_blueprint(institutions_blueprint)
    app.register_blueprint(requests_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(service_bluprint)
    app.register_blueprint(relation_blueprint)
    app.register_blueprint(configuration_blueprint)


    # API
    app.register_blueprint(auth_api_bp)
    app.register_blueprint(service_api_bp)
    app.register_blueprint(institution_api_bp)
    app.register_blueprint(user_api_bp)
    app.register_blueprint(services_types_api_bp)
    app.register_blueprint(solicitude_api_bp)
    app.register_blueprint(contact_api_bp)
    app.register_blueprint(notes_api_bp)

    database.init_app((app))

    app.register_error_handler(404, error.not_found_error)
    app.register_error_handler(401, error_401.unauthorized)

    @app.get("/")
    def admin():
        session['institutions'] = list_intitucions()
        session['contacto'] = config['inf_contacto']
        return render_template("home.html")
    
    @app.get("/home")
    def home():
        m = config['mantenimiento']
        user = session.get('user_id')
        print(session.get('user_id') )
        if m & (not check_user_role(user)):
            return render_template("mantenimiento.html")
        else:
            if check_user_role(user):
                institutions = list_intitucions()
            else:
                id_institutions =get_user_institutions(user)
                institutions = obtener_instituciones_por_ids(id_institutions)    
            session['institutions'] = institutions
            
            return render_template("layout.html")

    #Funciones para Jinja
    app.jinja_env.globals.update(is_authenticated = is_authenticated)

    #Funciones que crean comandos

    @app.cli.command(name="resetdb")
    def resetdb():
        database.reset_db()
        
    @app.cli.command(name="createdb")
    def createdb():
        database.create_db()

    @app.cli.command(name="seedsdb")
    def seedsdb():
        seeds.run()

    @app.cli.command(name="createdbseedsdb")
    def createdbseedsdb():
        database.reset_and_seed_db()


    @app.context_processor
    def utility_processor():
        def has_permission_wrapper(list_permitions):
            return has_permission_bool(list_permitions)

        return dict(has_permission_bool=has_permission_wrapper)
    
    return app
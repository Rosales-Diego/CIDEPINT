from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    '''Inicializacion de la aplicacion'''
    db.init_app(app)
    config_db(app)

def create_db():
    '''Crea la base de datos.'''
    print('Creando la base de datos')
    db.create_all()

def config_db(app):
    '''Configuracion de la aplicacion'''
    @app.teardown_request
    def close_session(execption=None):
        db.session.close()

def reset_db():
    '''Reseteo de la aplicacion'''
    #print('Reseteando la base de datos')
    db.drop_all()
    db.create_all()

def reset_and_seed_db():
    '''Reseteo y seed de la aplicacion'''
    reset_db()
    from src.core.seeds import run
    run()
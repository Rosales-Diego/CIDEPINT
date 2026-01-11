from datetime import datetime
from src.core.config.database import db
from enum import Enum

class Status(Enum):
        ACEPTED = "aceptada"  
        REJECTED = "rechazada"
        IN_PROCESS = "en_proceso" 
        FINISHED = "finalizada"
        CANCELED = "cancelada"

class TypeService(Enum):
        Análisis = "Análisis"  
        Consultoría = "Consultoría"
        Desarrollo = "Desarrollo"  

class Solicitude(db.Model):
    __tablename__ = "solicitudes"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.Enum(Status))
    type_of_service = db.Column(db.Enum(TypeService))
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.relationship('Note', backref='solicitude', lazy=True)

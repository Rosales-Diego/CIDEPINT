from datetime import datetime
from src.core.config.database import db
from enum import Enum



class Service(db.Model):
    
    __tablename__ = "services" 

    id = db.Column(db.Integer, primary_key=True, unique=True)
    
    name = db.Column(db.String(100))
    
    description = db.Column(db.String(50))
    
    search_keywords = db.Column(db.String(255))
    
    authorized_centers = db.Column(db.String(255))
    
    class TypeService(Enum):
        Análisis = "Análisis"  
        Consultoría = "Consultoría"
        Desarrollo = "Desarrollo"    
    
    type_of_service = db.Column(db.Enum(TypeService))
    
    enabled = db.Column(db.Boolean())
    
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    institutions_id = db.Column(db.Integer, db.ForeignKey('institutions.id'))
    
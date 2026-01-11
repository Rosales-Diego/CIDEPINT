from datetime import datetime
from src.core.config.database import db

class Note(db.Model):
    
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    solicitude_id = db.Column(db.Integer, db.ForeignKey('solicitudes.id'))
    
    content = db.Column(db.String(255))

    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)
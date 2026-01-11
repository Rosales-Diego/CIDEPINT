from datetime import datetime
from src.core.config.database import db

class Institution(db.Model):
    __tablename__ = "institutions"
    
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255))
    contact_info = db.Column(db.String(255))
    address = db.Column(db.String(255))
    location = db.Column(db.String(255))
    web = db.Column(db.String(255))
    active = db.Column (db.Boolean, default=True)
    key_words = db.Column(db.Text)
    work_schedule = db.Column(db.Text)

    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def get_by_id(cls, institution_id):
        """Obtiene una institución por su ID."""
        return cls.query.get(institution_id)

    @classmethod
    def create_new_instance(cls, name, contact_info, address, location, web, key_words, work_schedule):
        """Crea una nueva instancia de la institución y la agrega a la base de datos."""
        new_instance = cls(
            name=name,
            contact_info=contact_info,
            address=address,
            location=location,
            web=web,
            key_words=key_words,
            work_schedule=work_schedule
        )
        db.session.add(new_instance)
        db.session.commit()
        return new_instance

    
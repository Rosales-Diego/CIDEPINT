from datetime import datetime
from src.core.config.database import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column (db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column (db.String(100))
    name = db.Column (db.String(100))
    last_name = db.Column (db.String(100))
    active = db.Column (db.Boolean, default=True)

    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)

    institutions = db.relationship('Institution', secondary='user_institution_role', backref='users', viewonly=True)
    
    roles = db.relationship('Role', secondary='user_institution_role', backref='users', viewonly=True)


    


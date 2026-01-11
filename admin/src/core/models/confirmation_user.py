from datetime import datetime
from src.core.config.database import db
class ConfirmationUser(db.Model):

    id= db.Column (db.Integer, primary_key=True, unique=True)

    __tablename__ = "confirmation-user"


    email = db.Column(db.String(50), unique=True)
    token = db.Column (db.String(33))


    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)

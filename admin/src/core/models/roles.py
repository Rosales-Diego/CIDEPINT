from datetime import datetime
from src.core.config.database import db
from enum import Enum
from src.core.models.role_permission import RolePermission


class RoleEnum(Enum):
    SUPER_ADMIN = 'super_admin'
    ADMIN = 'admin'
    OPERATOR = 'operator'
    OWNER = 'owner'
    GENERAL_USER = 'general_user'
    

class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.Enum(RoleEnum), unique=True)
    
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)

    permissions = db.relationship('Permission', secondary='role_permission', back_populates='roles')
    
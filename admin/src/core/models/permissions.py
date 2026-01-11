from datetime import datetime
from src.core.config.database import db
from enum import Enum

permissions = {'User': ['user_index', 'user_new', 'user_destroy', 'user_update', 'user_show'],
                'Service': ['service_index', 'service_new', 'service_destroy', 'service_update', 'service_show'],
                'Institution': ['institution_index', 'institution_new', 'institution_destroy', 'institution_update', 'institution_show'],
                'Config': ['config_show', 'config_update']}

class Permission(db.Model):
    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), unique=True)

    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Define the relationship to Role via RolePermissions
    roles = db.relationship('Role', secondary='role_permission', back_populates='permissions')




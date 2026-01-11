from datetime import datetime
from src.core.config.database import db


# Define the RolePermissions association table
class RolePermission(db.Model):
    __tablename__ = 'role_permission'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'))
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id', ondelete='CASCADE'))
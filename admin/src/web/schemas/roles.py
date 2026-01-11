from marshmallow import Schema, fields, post_load
from src.web.schemas.permissions import PermissionSchema

class RoleSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    permissions = fields.Nested(PermissionSchema)

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)
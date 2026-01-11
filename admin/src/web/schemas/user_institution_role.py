from marshmallow import Schema, fields, post_load
from src.web.schemas.institutions import InstitutionSchema
from src.web.schemas.user import UserSchema
from src.web.schemas.roles import RoleSchema

class UserInstitutionRoleSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    institution_id = fields.Int()
    role_id = fields.Int()
    user = fields.Nested(UserSchema)
    
    institution = fields.Nested(InstitutionSchema)
    role = fields.Nested(RoleSchema)

user_institution_role_schema = UserInstitutionRoleSchema()
user_institution_roles_schema = UserInstitutionRoleSchema(many=True)
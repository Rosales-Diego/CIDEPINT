from marshmallow import Schema, fields, post_load
from src.web.schemas.institutions import InstitutionSchema
from src.web.schemas.roles import RoleSchema


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str()
    name = fields.Str()
    last_name =fields.Str()
    active = fields.Boolean()
    institutions = fields.Nested(InstitutionSchema)
    roles = fields.Nested(RoleSchema)
    inserted_at = fields.DateTime()
    # @post_load
    # def make_user(self, data, **kwargs):
    #     return User(**data)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

from marshmallow import Schema, fields, post_load
from src.web.schemas.services import ServiceSchema
from src.web.schemas.user import UserSchema
from enum import Enum
from src.core.models.solicitude import Solicitude, Status, TypeService

class StatusEnumField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.value

class TypeServiceEnumField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.value

class SolicitudeSchema(Schema):
    id = fields.Int(dump_only=True)
    service_id = fields.Int()
    user_id = fields.Int()
    status = StatusEnumField()
    comment = fields.String()
    type_of_service = TypeServiceEnumField()
    updated_at = fields.DateTime(dump_only=True)
    inserted_at = fields.DateTime(dump_only=True)
    
    institution_name = fields.String()
    service_name = fields.String()


class RequestListSchema(Schema):
    data = fields.Nested(SolicitudeSchema, many=True)
    page = fields.Int()
    per_page = fields.Int()
    total = fields.Int()
    institution_name = fields.String()
    service_name = fields.String()

solicitude_schema = SolicitudeSchema()
solicitudes_schema = RequestListSchema()




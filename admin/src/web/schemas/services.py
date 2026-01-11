from marshmallow import Schema, fields, post_load

class InstitutionSchema(Schema):
    id = fields.Int()
    name = fields.Str()

class ServiceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    description = fields.Str()
    search_keywords = fields.Str()
    authorized_centers = fields.Str()
    type_of_service = fields.Str()
    enabled = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    institutions_id = fields.Int(dump_only=True)
    
    # Agregar campos para la institución
    institution_name = fields.Str()
    
    
class ServiceListSchema(Schema):
    data = fields.Nested(ServiceSchema, many=True)
    page = fields.Int()
    per_page = fields.Int()
    total = fields.Int()


service_schema = ServiceSchema()
services_schema = ServiceListSchema()
institution_schema = InstitutionSchema()

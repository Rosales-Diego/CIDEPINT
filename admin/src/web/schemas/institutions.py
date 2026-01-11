from marshmallow import Schema, fields, post_load

class InstitutionSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    contact_info = fields.Str()
    address = fields.Str()
    location = fields.Str()
    web = fields.Str()
    active = fields.Boolean()
    key_words = fields.Str()
    work_schedule = fields.Str()
    updated_at = fields.DateTime()
    inserted_at = fields.DateTime()
    

institution_schema = InstitutionSchema()
institutions_schema= InstitutionSchema(many=True)
from marshmallow import Schema, fields

class NoteSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer()
    solicitude_id = fields.Integer()
    content = fields.String()
    updated_at = fields.DateTime(dump_only=True)
    inserted_at = fields.DateTime(dump_only=True)
    service_id = fields.Integer(dump_only=True)
    institution_name = fields.String()
    service_name = fields.String()
    
class NotesSchema(Schema):
    data = fields.Nested(NoteSchema, many=True)
    page = fields.Int()
    per_page = fields.Int()
    total = fields.Int()
    institution_name = fields.String()
    service_name = fields.String()


note_schema = NoteSchema()
notes_schema = NotesSchema()
from marshmallow import Schema, fields, post_load

class PermissionSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

permission_schema = PermissionSchema()
permissions_schema = PermissionSchema(many=True)
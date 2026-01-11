from marshmallow import Schema, fields, post_load
from enum import Enum
class TypeService(Enum):
        Análisis = "Análisis"  
        Consultoría = "Consultoría"
        Desarrollo = "Desarrollo"  

class ServiceTypeSchema(Schema):
    types = fields.Enum(TypeService)

services_type_schema = ServiceTypeSchema()
services_types_schema = ServiceTypeSchema(many=True)



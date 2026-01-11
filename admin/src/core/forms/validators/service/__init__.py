from wtforms import validators, ValidationError
from src.core.models.Institutional_Services.services import Service
from flask import Flask, session

def custom_length(min_length, max_length):
    def validate_length(form, field):
        if len(field.data) < min_length or len(field.data) > max_length:
            raise ValidationError(f'El campo debe tener entre {min_length} y {max_length} caracteres.')
    return validate_length

class UniqueServiceName: 
    def __init__(self, message="El nombre del servicio ya existe."):
        self.message = message

    def __call__(self, form, field):
        institution_id = session.get('institution_id')
        service = Service.query.filter_by(name=field.data,institutions_id=institution_id).first()
        if service is not None:
            raise ValidationError(self.message)
# Importo el formulario de flask_wtf
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField
from wtforms.validators import DataRequired ,Regexp
from src.core.models.Institutional_Services.services import Service
from src.core.forms.validators.service import custom_length,UniqueServiceName

# Clase del formulario para crear instituciones
class ServiceForm(FlaskForm):
    
    name = StringField('Nombre', validators=[DataRequired(), 
                                             custom_length(1, 200),
                                             Regexp(r'^[a-zA-Z0-9\s]+$',
                                                    message="El nombre no puede contener caracteres especiales"),
                                             UniqueServiceName(message="El nombre del servicio ya existe.")])
    
    description = StringField('Descripción' ,
                              validators=[custom_length(10, 255)]
                              ,description="Ingrese una descripción de 10 a 255 caracteres.")
    
    search_keywords = StringField('Palabras Clave' , 
                                  validators=[custom_length(5, 255)],
                                  description="Las palabras claves tiene que ir en este formato '{' PalabraClave1,PalabraClaveN'}'.")
    
    authorized_centers = StringField('Centros Autorizados',
                                     validators=[custom_length(5, 255)],
                                     description="Las centros autorizados tiene que ir en este formato '{' Centro1,CentroN'}'.")
    
    type_of_service = SelectField('Tipo de Servicio', 
                                  choices=[(choice.value, choice.value) for choice in Service.TypeService])
    
    enabled = BooleanField('Habilitado')
    
    
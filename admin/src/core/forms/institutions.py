# Importo el formulario de flask_wtf
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, URLField, RadioField
from wtforms import validators
from wtforms import widgets

# Clase del formulario para crear instituciones
class InstitutionForm(FlaskForm):
    nombre = StringField("Nombre", validators=[
                                validators.DataRequired(message="Debe ingresar un nombre"),
                                validators.Length(min=3, max=50, message="El nombre debe tener entre 3 y 50 caracteres")],
                                description="Nombre de la institucion",
                                id="nombre")
    
    localizacion = StringField("Localización", 
                                validators=[validators.DataRequired(message="Debe ingresar una localización"),
                                validators.Length(min=5, max=50, message="La localización debe tener entre 10 y 50 caracteres")],
                                description="Localizacion",
                                id="localizacion")
    
    direccion = StringField("Dirección", 
                                validators=[validators.DataRequired(message="Debe ingresar una dirección"), 
                                validators.Length(min=5, max=50, message="La dirección debe tener entre 10 y 50 caracteres")],
                                description="Direccion de la institucion",
                                id="direccion")
    web = URLField("Pagina web", validators=[validators.DataRequired(message="Debe ingresar una URL"), 
                                    validators.URL(message="Debe ingresar una URL valida")],
                                    description="Pagina web de la institucion",
                                    id="web")
    palabras_claves = StringField("Palabras Claves", 
                                validators=[validators.DataRequired(message="Debe ingresar al menos una palabra clave"), 
                                validators.Length(min=10, max=255, message="Las palabras claves deben tener entre 10 y 255 caracteres"),
                                validators.Regexp("^[a-zA-Z0-9_, ]*$", message="Las palabras claves deben ser alfanumerico")],
                                description="Palabras claves de la institucion",
                                id="palabras_claves")
    descripcion = StringField("Descripción", 
                                validators=[validators.DataRequired(message="Debe ingresar una descripción"),
                                validators.Length(min=10, max=255, message="La descripción debe tener entre 10 y 255 caracteres")],
                                description="Descripcion de la institucion",
                                id="descripcion") 
    horario = StringField("Dias y horarios de atencion", validators=[validators.DataRequired(message="Debe ingresar un horario"), 
                                     validators.Length(min=10, max=100, message="El horario debe tener entre 10 y 100 caracteres")],
                                     description="Dias y horarios de atencion",
                                     id="horario")
    estado = RadioField("Estado", choices=[('habilitado', 'Habilitado'), 
                                           ('deshabilitado', 'Deshabilitado')], 
                                           validators=[validators.DataRequired(message="Debe seleccionar un estado")],
                                           widget=widgets.TableWidget(with_table_tag=True))
    telefono = StringField("Teléfono", validators=[validators.DataRequired(), 
                                         validators.Length(min=7, max=10, message="El teléfono debe tener entre 7 y 10 dígitos"),
                                         validators.Regexp("^[0-9]*$", message="El teléfono debe ser un número")],
                                         description="Telefono de la institucion",
                                         id="telefono")

    
                                             
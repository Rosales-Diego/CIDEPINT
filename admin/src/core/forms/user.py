from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField,ValidationError
from wtforms import validators
from wtforms import widgets
from src.core.models import User
class UserForm(FlaskForm):
    email = StringField("Email", validators=[
        validators.DataRequired(message="Debe ingresar un email"),
        validators.Email(message="Debe ingresar un email válido")
    ], description="Correo electrónico", id="email")

    password = PasswordField("Contraseña", validators=[
        validators.DataRequired(message="Debe ingresar una contraseña"),
    ], description="Contraseña", id="password")

    name = StringField("Nombre", validators=[
        validators.DataRequired(message="Debe ingresar un nombre"),
        validators.Length(max=100, message="El nombre debe tener menos de 100 caracteres")
    ], description="Nombre", id="name")

    last_name = StringField("Apellido", validators=[
        validators.DataRequired(message="Debe ingresar un apellido"),
        validators.Length(max=100, message="El apellido debe tener menos de 100 caracteres")
    ], description="Apellido", id="last_name")

    active = RadioField("Activo", choices=[('activo', 'Activo'), 
                                           ('inactivo', 'Inactivo')], 
                                           validators=[validators.DataRequired(message="Debe seleccionar un estado")],
                                           widget=widgets.TableWidget(with_table_tag=True))
    
class UpdateUserForm(UserForm):
    # Hereda todos los campos de UserForm, excepto 'password'

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        # Elimina el campo de contraseña
        del self.password



from src.core.models.users import User
from src.core.models.roles import Role
from src.core.models.user_institution_role import UserInstitutionRole
from src.core.seeds import create_user_institution_role
from src.core import auth
from src.core.auth import list_users

from src.web.helpers.auth import login_required
from src.web.helpers.auth import has_permission 
from src.web.helpers.auth import in_maintenance
from src.web.helpers import paging
from src.web.helpers.user import fill_form_with_user, fill_update_form_with_user

from src.core.forms.user import UserForm, UpdateUserForm

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session

from src.core.models import create_user_with_form
from src.core.models import find_user_by_id
from src.core.models import find_user_by_email
from src.core.models import exist_mail
from src.core.models import delete_user
from src.core.models import update_user_with_form
from src.core.config.database import db

user_blueprint = Blueprint("users", __name__, url_prefix="/usuarios")


@user_blueprint.route("/", methods=["GET", "POST"])
@login_required
def index():
    """
    La ruta .../usuarios me muestra el listado de los usuarios
    si el usuario superadmin tiene permiso de index  
    """
    
    if not has_permission(["user_index"]):
        flash("Usted no tiene permiso para ver esta pagina", "error")
        return redirect(url_for("auth.login"))
    else: 

        query = User.query

        email = request.form.get('email')
        activo = request.form.get('activo')

        print("Activo: ", activo)
        if activo is not None:
            if activo.lower() == 'activo':
                query = query.filter(User.active == True)
            elif activo.lower() == 'bloqueado':
                query = query.filter(User.active == False)

        # Filtra por email si se proporciona
        if email:
            query = query.filter(User.email.ilike(f'%{email}%'))

        encontrados = query.all()
        

        page = request.args.get('page', type=int, default=1)

        #Paso todos los elementos a la función y que eso me devuelva según la configuración
        users = paging.paginate(list_users(), page)
        total_pages = paging.get_total_pages(list_users(), page)

        encontrados = paging.paginate(encontrados, page)
        
    
        return render_template("users/index.html", users=users, page = page, total_pages = total_pages, encontrados = encontrados)

@user_blueprint.get("/show/<int:id>")
@in_maintenance
@login_required
def show(id):
    """
    La ruta .../usuarios/show me muestra información de un usuario
    de la cual se pasa el nombre por parametro
    si el usuario superadmin tiene permiso show  
    """  
    if not has_permission(["user_show"]):
        flash("Usted no tiene permiso para ver esta pagina", "error")
        return redirect("/")
    else: 
        user = find_user_by_id(id)
        return render_template("/users/show.html", user=user)
        

@user_blueprint.route("/editar/<int:id>", methods=["GET"])
@in_maintenance
@login_required
def get_update(id):
    """
    La ruta .../usuarios/update me permite modificar la información de
    una usuario, cuyo nombre se recibe por parametro
    si el usuario superadmin tiene permiso update 
    """
    if not has_permission(["user_update"]):
        flash("Usted no tiene permiso para ver esta pagina", "error")
        return redirect(url_for("users.index")) #users.index ->"usuarios.index"
    else: 
        user = find_user_by_id(id)
        form = UpdateUserForm()
        form = fill_update_form_with_user(form, user)
        
        form.process()
       
        return render_template("/users/update.html", form=form, user=user)


@user_blueprint.post("/editar/<int:id>")
@in_maintenance
@login_required
def update(id):
    """
    La ruta .../usuarios/editar me permite editar una usuario  
    """
    if not has_permission(["institution_update"]):
        flash("Usted no tiene permiso para ver esta pagina", "error")
        return redirect(url_for("home"))
    else: 
        form = UpdateUserForm()
        user = find_user_by_id(id)
        email_user_old = find_user_by_id(id).email
        new_email = form.email.data

        if new_email != email_user_old:
            if exist_mail(new_email):
                flash("El nombre de email ya esta en uso, elija otro", "error")
                return render_template("/users/update.html", form=form)
        
        if form.validate():
            #Actualizo todos los campos del usuario con los datos del formulario
            update_user_with_form(user, form)

            flash('Usuario actualizado exitosamente', 'success')
            return redirect(url_for("users.index"))
        else:
            flash("Se encontraron errores en el formulario. Por favor, corrige los errores e intenta nuevamente.", "error")

            return render_template("/users/update.html", form=form, user=user)


@user_blueprint.route("/crear", methods=['GET', 'POST'])
@login_required
def get_create():
    """
    La ruta .../usuarios/crear permite generar una petición para crear un usuario
    si el usuario superadmin tiene el permiso "user_create".
    """
    if not has_permission(["user_new"]):
        flash("Usted no tiene permiso para ver esta página", "error")
        return redirect(url_for("home"))
    else:
        form = UserForm()

        if form.validate_on_submit():
            #En realidad esto nunca se ejecuta, solo es decorativo
            flash("Usuario creado con éxito", "success")
            return redirect(url_for("users.index")) 

        #A partir del template se lo redirige a create()
        return render_template("users/create.html", form=form)


    
@user_blueprint.post("/create")
@in_maintenance
@login_required
def create():
    """
    La ruta .../usuarios/crear me permite crear una usuario  
    """
    if not has_permission(["institution_new"]):
        flash("Usted no tiene permiso para ver esta pagina", "error")
        return redirect(url_for("home"))
    else: 
        form = UserForm()
        if exist_mail(form.email.data):
            flash("El nombre de email ya esta en uso, elija otro", "error")
            return render_template("/users/create.html", form=form)
        elif form.validate(): 
            create_user_with_form(form)
            flash("La usuario se creó correctamente", "success")
            return redirect(url_for("users.index"))
        else:
            return render_template("/users/create.html", form=form)


@user_blueprint.route("/destroy/<int:id>")
@in_maintenance
@login_required
def destroy(id):
    """
    La ruta .../usuarios/ me permite eliminar una usuario
    si el usuario superadmin inició sesión y tiene permiso destroy  
    """
    if not has_permission(["institution_destroy"]):
        flash("Usted no tiene permiso para ver esta pagina", "error")
        return redirect("/home")
    else: 
        user = find_user_by_id(id)

        if user:
            success = delete_user(user)

            if success:
                flash("El usuario se eliminó correctamente", "error")
            else:
                flash("No es posible eliminar este usuario", "success")
        else:
            flash("El usuario no existe", "error")
        return redirect(url_for("users.index"))
        

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session

from src.web.helpers.auth import login_required, has_permission, in_maintenance
from src.web.helpers.institutions import fill_form_with_institution

from src.core.models import get_institutions , validate_location
from src.core.models import create_institution
from src.core.models import find_institution_by_name
from src.core.models import find_institution_by_id
from src.core.models import update_institution
from src.core.models import delete_institution
from src.core.models import get_service_for_institution

from src.web.helpers import paging

from src.core.config.database import db
from src.core.forms.institutions import InstitutionForm
from src.core.models import Institution

"""
Agrego un blueprint nuevo para las instituciones.
uso el prefijo /instituciones para todo el controlador
"""
institutions_blueprint = Blueprint("institutions", __name__, url_prefix="/instituciones")

@in_maintenance
@institutions_blueprint.get("/")
@login_required
def list_institutions():
    """
    La ruta .../instituciones/ me muestra el listado de instituciones
    si el usuario superadmin tiene permiso de index  
    """

    if not has_permission(["institution_index"]):
        flash("Usted no tiene permiso para ver esta pagina", "error")
        return redirect(url_for("auth.login"))
    else: 
        page = request.args.get('page', type=int, default=1)

        claves = request.form.get('claves')
        #Desarrollar filtrar por clave

        #Paso todos los elementos a la función y que eso me devuelva según la configuración
        instituciones = paging.paginate(get_institutions(), page)
        total_pages = paging.get_total_pages(get_institutions(), page)
        
        return render_template("/institutions/index.html", items=instituciones, page = page, total_pages = total_pages)


@institutions_blueprint.get("/show/<int:id>")
@in_maintenance
@login_required
def show(id):
    """
    La ruta .../instituciones/show me muestra información de una institucion
    de la cual se pasa el nombre por parametro
    si el usuario superadmin tiene permiso show  
    """  
    if not has_permission(["institution_show"]):
        flash("Usted no tiene permiso para ver esta pagina", "error")
        return redirect("/")
    else: 

        page = request.args.get('page', type=int, default=1)

        #Paso todos los elementos a la función y que eso me devuelva según la configuración
        services = paging.paginate(get_service_for_institution(id), page)
        total_pages = paging.get_total_pages(get_service_for_institution(id), page)
        institution = find_institution_by_id(id)
        

        return render_template("/institutions/show.html", institution=institution, items=services, page = page, total_pages = total_pages)
        

@institutions_blueprint.route("/editar/<int:id>", methods=["GET"])
@in_maintenance
@login_required
def get_update(id):
    """
    La ruta .../instituciones/update me permite modificar la información de
    una institucion, cuyo nombre se recibe por parametro
    si el usuario superadmin tiene permiso update 
    """
    if not has_permission(["institution_update"]):
        flash("Usted no tiene permiso para ver esta pagina", "error")
        return redirect(url_for("instituciones.index"))
    else: 
        institution = find_institution_by_id(id)
        form = InstitutionForm()
        form = fill_form_with_institution(form, institution)
        
        form.process()
       
        return render_template("/institutions/update.html", form=form, institucion=institution)


@institutions_blueprint.route("/editar/<int:id>", methods=['GET', 'POST'])
@in_maintenance
@login_required
def update(id):
    """
    La ruta .../instituciones/editar me permite editar una institución  
    """
    if not has_permission(["institution_update"]):
        flash("Usted no tiene permiso para ver esta pagina", "error")
        return redirect(url_for("home"))

    form = InstitutionForm()
    institucion = find_institution_by_id(id)

    try:
        if form.validate_on_submit():
            estado = form.estado.data == "habilitado"

            institucion.name = form.nombre.data
            institucion.address = form.direccion.data
            institucion.location = validate_location(form.localizacion.data)
            institucion.contact_info = form.telefono.data
            institucion.web = form.web.data
            institucion.work_schedule = form.horario.data
            institucion.key_words = form.palabras_claves.data
            institucion.info = form.descripcion.data
            institucion.active = estado
            
            db.session.commit()
            flash("La institución se modificó correctamente", "success")
            return redirect(url_for("institutions.list_institutions"))

        # Si llegamos aquí, significa que el formulario no se envió o no es válido
        flash("Se encontraron errores en el formulario. Por favor, corrige los errores e intenta nuevamente.", "error")
        return render_template("/institutions/update.html", form=form, institucion=institucion)

    except ValueError as e:
        # Capturar la excepción ValueError y manejarla aquí
        flash(f"Error: {str(e)}", "error")
        return render_template("/institutions/update.html", form=form, institucion=institucion)


@institutions_blueprint.route("/crear", methods=['GET', 'POST'])
@login_required
def get_create():
    """
    La ruta .../instituciones/crear permite generar una petición para crear una institución
    si el usuario superadmin tiene el permiso "institution_create".
    """
    if not has_permission(["institution_new"]):
        flash("Usted no tiene permiso para ver esta página", "error")
        return redirect(url_for("home"))
    else:
        form = InstitutionForm()

        if form.validate_on_submit():
            # Crea una nueva instancia de Institution con los datos del formulario
            
            try:
                new_institution = Institution(
                    name=form.nombre.data,
                    contact_info=form.telefono.data,
                    address=form.direccion.data,
                    location=validate_location(form.localizacion.data),
                    web=form.web.data,
                    active=form.estado.data == 'habilitado',
                    key_words=form.palabras_claves.data,
                    work_schedule=form.horario.data
                )      
                print(form.localizacion.data , new_institution.location)
                # Agrega la nueva institución a la base de datos
                db.session.add(new_institution)
                db.session.commit()

                flash("Institución creada con éxito", "success")
                return redirect(url_for("institutions.list_institutions"))  # Ajusta esto según tu configuración
            except ValueError as e:
                # Capturar la excepción ValueError y manejarla aquí
                flash(f"Error: {str(e)}", "error")
                return render_template("institutions/create.html", form=form)
        return render_template("institutions/create.html", form=form)


    
@institutions_blueprint.post("/create")
@in_maintenance
@login_required
def create():
    """
    La ruta .../instituciones/crear me permite crear una institución  
    """

    if not has_permission(["institution_new"]):
        flash("Usted no tiene permiso para ver esta pagina", "error")
        return redirect(url_for("home"))
    else: 
        form = InstitutionForm()
        if form.validate(): 
            estado=form.estado.data == "habilitado"

            #info=form.descripcion.data,
            create_institucion(
                name=form.nombre.data, 
                address=form.direccion.data,
                location=form.localizacion.data, 
                contact_info=form.telefono.data,
                web=form.web.data, 
                work_schedule=form.horario.data,
                key_words=form.palabras_claves.data, 
                 
                active=estado)
            flash("La institución se creó correctamente", "success")
            return redirect(url_for("instituciones.index"))
        else:
            return render_template("/institutions/instituciones_create.html", form=form)


@institutions_blueprint.route("/destroy/<int:id>")
@in_maintenance
@login_required
def destroy(id):
    """
    La ruta .../instituciones/ me permite eliminar una institución
    si el usuario superadmin inició sesión y tiene permiso destroy  
    """
    if not has_permission(["institution_destroy"]):
        flash("Usted no tiene permiso para ver esta pagina", "error")
        return redirect("/home")
    else: 
        institution = find_institution_by_id(id)

        if institution:
            delete_institution(institution)
            flash("La institución se eliminó correctamente", "success")
        else:
            flash("La institución no existe", "error")
        return redirect(url_for("institutions.list_institutions"))
        
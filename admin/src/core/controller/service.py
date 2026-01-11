from flask import Blueprint , flash
from src.core.config.database import db
from flask import render_template,request,redirect, url_for
from datetime import datetime
#para el paginado
from src.web.helpers import paging
from flask import session
from src.web.helpers.auth import login_required , has_permission ,in_maintenance 
import re

from src.core.models.solicitude import Solicitude
from src.core.models.note import Note
from src.core.models.Institutional_Services.services import Service
from src.core.controller.error_service import validator ,validator_update

from src.core.models import list_service , get_service, get_request_to, get_me_notes_for_service , get_notes_Solicitud
from src.core.forms.service import ServiceForm


service_bluprint = Blueprint("service",__name__,url_prefix="/service")



@service_bluprint.route("/add_comment/<int:service_id>/<int:request_id>", methods=['POST'])
@in_maintenance
@login_required
def add_comment(service_id, request_id):
    if not has_permission(["service_show"]):
        flash("Usted no tiene permiso para agregar comentarios", "error")
        return redirect(url_for("auth.login"))

    comment = request.form.get('comment')
    user_id =  session.get('user_id')

    if comment:
        solicitude = Solicitude.query.get(request_id)
        if solicitude:
            note = Note(
                user_id = user_id,
                solicitude_id = solicitude.id,
                content = comment)
            db.session.add(note)
            db.session.commit()
            
            flash("Comentario agregado exitosamente", "success")
        else:
            flash("La solicitud no fue encontrada", "error")

    solicitude = Solicitude.query.get(request_id)
    
    
    return redirect(url_for("service.show_request", service_id=service_id))



#index
@service_bluprint.route("/show_requests/<int:service_id>", methods=['GET', 'POST'])
@in_maintenance
@login_required
def show_request(service_id):
    if not has_permission(["service_show"]):
        flash("Usted no tiene permiso para ver esta pagina", "error")
        return redirect(url_for("auth.login"))

    page = request.args.get('page', type=int, default=1)
    user_id = session.get('user_id')
    
    requests = paging.paginate(get_request_to(service_id), page)
    
    total_pages = paging.get_total_pages(get_request_to(service_id), page)
    print(requests)
    return render_template("services/show_requests.html", requests=requests,page=page,total_pages=total_pages)


#mostrarNotas
@service_bluprint.route("/show_notas/<int:solicitud_id>", methods=['GET'])
@in_maintenance
@login_required
def show_notas(solicitud_id):
    if not has_permission(["service_show"]):
        flash("Usted no tiene permiso para ver esta pagina", "error")
        return redirect(url_for("auth.login"))
 
    notes = get_notes_Solicitud(solicitud_id)
    user_id = session.get('user_id')
        
    return render_template("services/show_notas.html", notes=notes, current_user=user_id, solicitud_id=solicitud_id)

#crear \Nota
@service_bluprint.route("/show_notas/<int:solicitud_id>", methods=['POST'])
@in_maintenance
@login_required
def show_notas_add(solicitud_id):
    if not has_permission(["service_show"]):
        flash("Usted no tiene permiso para agregar comentarios", "error")
        return redirect(url_for("auth.login"))

    comment = request.form.get('comment')
    user_id =  session.get('user_id')

    if comment and solicitud_id:
        note = Note(
            user_id = user_id,
            solicitude_id = solicitud_id,
            content = comment)
        db.session.add(note)
        db.session.commit()
            
        flash("Comentario agregado exitosamente", "success")
    else:
        flash("La solicitud no fue encontrada", "error")

    notes = get_notes_Solicitud(solicitud_id)
    return render_template("services/show_notas.html", notes=notes , current_user=user_id, solicitud_id=solicitud_id)

#index
@service_bluprint.route("/list/<int:institution_id>", methods=['GET', 'POST'])
@in_maintenance
@login_required
def list_services(institution_id):
    
    if not has_permission(["service_index"]):
        flash("Usted no tiene permiso para ver esta pagina", "error")
        return redirect(url_for("auth.login"))

    page = request.args.get('page', type=int, default=1)
    user_id = session.get('user_id')
    
    if request.method == 'POST':
        session.pop('institution_id', None)
        institution_id = request.form.get('institution_id')
    
    services = paging.paginate(list_service(institution_id), page)
    total_pages = paging.get_total_pages(list_service(institution_id), page)
    
    return render_template("services/list.html", services=services,user_id=user_id,institution_id=institution_id,page=page,total_pages=total_pages)

#show
@service_bluprint.route("/show/<int:service_id>/<int:user_id>", methods=['GET', 'POST'])
@in_maintenance
@login_required
def show(service_id,user_id):

    if not has_permission(["service_show"]):
        flash("Usted no tiene permiso para ver esta pagina", "error")
        return redirect(url_for("auth.login"))

    service = get_service(service_id)
    user_id = request.form.get('user_id')
    Key_List = re.sub(r'[{}]', '', service.search_keywords)
    keywords_list = Key_List.split(",")  # Convierte la cadena en una lista
    Cent_list = re.sub(r'[{}]', '', service.authorized_centers)
    Centers_list = Cent_list.split(",")
    return render_template("services/show.html", service=service , list_key=keywords_list , list_cent=Centers_list ,user_id=user_id)

#update
@service_bluprint.route('/update/<int:service_id>', methods=['GET', 'POST'])
@login_required
def update(service_id):

    if not has_permission(["service_update"]):
        flash("Usted no tiene permiso para ver esta pagina", "error")
        return redirect(url_for("auth.login"))

    service = get_service(service_id)
    institution_id = service.institutions_id
    session['institution_id'] = institution_id
    
    form = ServiceForm(obj=service)

    if request.method == 'POST' and form.validate():
        form.populate_obj(service)
        service.updated_at = datetime.utcnow()
        db.session.commit()
        return 'Servicio modificado con éxito'
    return render_template("services/update.html", form=form, servicio=service)

#crerate
@service_bluprint.route("/create/<int:institution_id>",methods=['GET', 'POST'])
@login_required
def create(institution_id):

    #if not has_permission(["service_new"]):
        #flash("Usted no tiene permiso para ver esta pagina", "error")
        #return redirect(url_for("auth.login"))

    form = ServiceForm()
    
    institution_id = session.get('institution_id')
    
    if form.validate_on_submit():
        nuew_service = Service(
            name=form.name.data,
            description=form.description.data,
            search_keywords=form.search_keywords.data,
            authorized_centers=form.authorized_centers.data,
            type_of_service=form.type_of_service.data,
            enabled=form.enabled.data,
            institutions_id = institution_id
        )
        db.session.add(nuew_service)
        db.session.commit()
        flash("Servico creada con éxito", "success")
        return redirect(url_for('service.list_services',institution_id = institution_id))
    
    return render_template("services/create.html", institution_id=institution_id , form=form)


#destroy
@service_bluprint.route("/destroy/<int:service_id>")
@login_required
def destroy(service_id):
    #if not has_permission(["service_destroy"]):
        #flash("Usted no tiene permiso para ver esta pagina", "error")
        #return redirect(url_for("auth.login"))

    servicio = Service.query.get(service_id)
    
    if servicio:
        # Si se encuentra el servicio, elimínalo de la base de datos
        db.session.delete(servicio)
        db.session.commit()
        flash("Servicio eliminado correctamente", 'success')
    else:
        flash("No se encontró el servicio", 'error')
        
    return redirect(url_for('service.list_services', institution_id= servicio.institutions_id))
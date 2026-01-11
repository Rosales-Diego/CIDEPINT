from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session

from src.web.helpers.auth import login_required, has_permission, in_maintenance

from src.core.models import get_me_requests 

from src.web.helpers import paging

from src.core.config.database import db
from src.core.models.solicitude import Solicitude

"""
Agrego un blueprint nuevo para las solicitudes de cada uno de los usuarios.
uso el prefijo /me_requests para todo el controlador
"""
requests_blueprint = Blueprint("requests", __name__, url_prefix="/me_requests")

@in_maintenance
@requests_blueprint.get("/")
@login_required
def list_me_requests():

    page = request.args.get('page', type=int, default=1)


    #Paso todos los elementos a la función y que eso me devuelva según la configuración
    user_id = session.get('user_id')
    my_requests = paging.paginate(get_me_requests(user_id), page)
    total_pages = paging.get_total_pages(get_me_requests(user_id), page)
        
    return render_template("/request/index.html", items=my_requests, page = page, total_pages = total_pages)

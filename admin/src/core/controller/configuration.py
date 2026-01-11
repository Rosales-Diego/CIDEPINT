from src.web.helpers.role import login_required
from src.core.config.database import db
from src.core.models.institutions import Institution
from src.core.models.roles import Role
from src.core.models.user_institution_role import UserInstitutionRole
from src.core.models.users import User
from flask import Blueprint, flash, request, render_template, session, redirect, url_for
from src.core import auth
from src.web.configs import config
from src.web.helpers.auth import has_permission 

configuration_blueprint = Blueprint("configuration", __name__, url_prefix="/configuration")

@login_required
@configuration_blueprint.route("/", methods=('GET', 'POST'))
def index():

    if not has_permission(["config_show"]):
        flash("Usted no tiene permiso para ver esta pagina", "error")
        return redirect(url_for("auth.login"))

    m = config['mantenimiento']
    cantpag = config['cantRegPags']
    inf = config['inf_contacto']
    session['contacto'] = inf
    return render_template("/config/config.html",m=m,cantpag=cantpag,inf=inf)


@configuration_blueprint.route("/configm1", methods=('GET', 'POST'))
def configm1():

    '''Pone la web en funcionamiento'''

    config['mantenimiento'] = False
    return redirect("/configuration/")

@configuration_blueprint.route("/configm2", methods=('GET', 'POST'))
def configm2():

    '''Pone la web en mantenimiento'''

    if not has_permission(["config_update"]):
        flash("Usted no tiene permiso para ver esta pagina", "error")
        return redirect(url_for("auth.login"))

    config['mantenimiento'] = True
    return redirect("/configuration/")


@configuration_blueprint.route("/configp", methods=('GET', 'POST'))
def configp():

    '''Modifica la cantidad de elemantos mostrados por página'''

    if not has_permission(["config_update"]):
        flash("Usted no tiene permiso para ver esta pagina", "error")
        return redirect(url_for("auth.login"))

    config['cantRegPags'] = request.form.get('cantpag')
    return redirect("/configuration/")


@configuration_blueprint.route("/configi", methods=('GET', 'POST'))
def configi():

    '''Modifica el mansaje de informacion de contacto'''

    if not has_permission(["config_update"]):
        flash("Usted no tiene permiso para ver esta pagina", "error")
        return redirect(url_for("auth.login"))

    config['inf_contacto'] = request.form.get('inf')
    return redirect("/configuration/")

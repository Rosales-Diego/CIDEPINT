from src.web.helpers import paging
from src.web.helpers.auth import has_permission
from src.web.helpers.role import login_required
from src.core.config.database import db
from src.core.models.institutions import Institution
from src.core.models.roles import Role
from src.core.models.user_institution_role import UserInstitutionRole
from src.core.models.users import User
from src.core.seeds import create_user_institution_role, update_user_institution_role
from flask import Blueprint, flash, request, render_template, redirect, url_for
from src.core.auth import find_user_by_email_and_pass

relation_blueprint = Blueprint("relation", __name__, url_prefix="/relation")

@login_required
@relation_blueprint.route("/index/<int:institution_id>", methods=('GET', 'POST'))
def update(institution_id):
    if not has_permission(["user_index","user_update","user_destroy"]):
        flash("Usted no tiene permiso para ver esta pagina", "error")
        return redirect(url_for("auth.login"))
      
    users = User.query.join(UserInstitutionRole).join(Institution).\
        filter(UserInstitutionRole.institution_id == Institution.id , Institution.id == institution_id, User.id == UserInstitutionRole.user_id).all()
    insName = Institution.query.filter_by(id=institution_id).first()
    roles = Role.query.all()
    email = request.form.get('email')
    usub = User.query.filter_by(email=email).first()
    usubRol = None

    page = request.args.get('page', type=int, default=1)
    total_pages = paging.get_total_pages(users, page)
    users = paging.paginate(users, page)

    if usub:
        usubRol = UserInstitutionRole.query.filter_by(user_id = usub.id ,institution_id=institution_id).first()
    if request.method == 'POST':
        if email != '':
            if usub:
                idUsuBuscado = usub.id
                usubRol = UserInstitutionRole.query.filter_by(user_id = idUsuBuscado ,institution_id=institution_id).first()
                if usubRol:
                    actualizar = request.form.get('Actualizar')
                    if actualizar == 'Actualizar':
                        update_user_institution_role(usubRol=usubRol, newRol=request.form.get('newRol'))
                        flash("Se actualizó correctamente el rol del usuario en esta institución", "success")
                        return render_template("/user_rol_inst/index.html", usub=usub, users=users, ins=institution_id, roles=roles, insName=insName, usubRol=usubRol, page=page, total_pages=total_pages)
                    eliminar = request.form.get('Eliminar')
                    if eliminar == 'Eliminar':
                        db.session.delete(usubRol)
                        db.session.commit()
                        flash("Se eliminó correctamente el rol del usuario en esta institución", "success")
                        return render_template("/user_rol_inst/index.html", usub=usub, users=users, ins=institution_id, roles=roles, insName=insName, usubRol=usubRol, page=page, total_pages=total_pages)
                else:
                    flash("El usuario buscado no tiene rol en esta institución", "error")
            else:
                flash("El usuario buscado no existe", "error")
    return render_template("/user_rol_inst/index.html", usub=usub, users=users, ins=institution_id, roles=roles, insName=insName, usubRol=usubRol, page=page, total_pages=total_pages)

@relation_blueprint.route("/new/<int:institution_id>", methods=('GET', 'POST'))
def new(institution_id):
    if not has_permission(["user_new"]):
        flash("Usted no tiene permiso para ver esta pagina", "error")
        return redirect(url_for("auth.login"))

    roles = Role.query.all()
    role=None
    new_rol = request.form.get('new_rol')
    inst = Institution.query.filter_by(id=institution_id).first()
    email = request.form.get('email')
    userb = find_user_by_email_and_pass(email)
    if request.method == 'POST':
        if email != '':
            btnBuscar = request.form.get('Buscar')
            if btnBuscar == 'Buscar':
                # Busca el usuario por email
                if not userb:
                    flash("No se encontró el usuario buscado", "error")
                else:
                    usuarios_con_roles = UserInstitutionRole.query.filter(userb.id==UserInstitutionRole.user_id, UserInstitutionRole.institution_id == institution_id).first()
                    if usuarios_con_roles:
                        role = usuarios_con_roles.role_id
                        flash("Usuario buscado ya tiene rol en esta institucion", "error")
                        return render_template("/user_rol_inst/new.html", userb=userb, institution_id=institution_id, new_rol=new_rol,inst_name=inst.name,email=email,role=role, roles=roles)
                    else:
                        flash("Usuario buscado encontrado", "success")
                        return render_template("/user_rol_inst/new.html", userb=userb, institution_id=institution_id, new_rol=new_rol,inst_name=inst.name,email=email,role=role, roles=roles)

            btn = request.form.get('Crear')                
            if btn == 'Crear':
                new_rol = request.form.get('new_rol')
                flash("Se asignó el nuevo rol", "success")
                create_user_institution_role(user_id=userb.id, institution_id=institution_id, role_id=request.form.get('new_rol'))
                return render_template("/user_rol_inst/new.html", userb=userb, institution_id=institution_id, new_rol=new_rol,inst_name=inst.name,email=email,role=role, roles=roles)
    return render_template("/user_rol_inst/new.html", userb=userb,institution_id=institution_id,new_rol=new_rol,inst_name=inst.name,email=email,role=role, roles=roles)

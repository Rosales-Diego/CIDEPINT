from flask import Blueprint
from src.core.models.solicitude import Solicitude, Status, TypeService
from src.core.models.note import Note
from src.core.models.institutions import Institution
from src.core.models.users import User
from src.core.models.Institutional_Services.services import Service
from src.core.config.database import db

from flask import session, jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.web.schemas.solicitude import solicitude_schema, solicitudes_schema
from src.web.schemas.notes import notes_schema,note_schema

from src.core.models import get_me_notes, get_names_services, get_notes_service, get_me_notes_for_service

notes_api_bp = Blueprint("notes", __name__, url_prefix="/api/notes")


@jwt_required()
@notes_api_bp.get("/me_notes/")
def list_me_notes():
    """
    Lista las notas hechas por un usuario a un servicio
    """

    try:
        if request.method == "OPTIONS":
            return make_response()
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        order = request.args.get('order', 'desc')
        
        user_id = get_jwt_identity()
        # user_id = 1
            
        notes = get_me_notes(user_id)
        
        notes_with_service_name = get_names_services(notes)
        
        total = len(notes_with_service_name)

        # Calcular el índice de inicio y final para la paginación
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page

        notes_data = notes_with_service_name[start_idx:end_idx]

        
        result = notes_schema.dump({'data': notes_data, 'page': page, 'per_page': per_page, 'total': total})
        
        return result, 200
    except Exception as e:
        return {"error": str(e)}, 401
    
    
@jwt_required()
@notes_api_bp.get("/notes_solicitude")
def list_notes_solicitude():
    """
    Lista las notas hechas a un servicio
    """

    try:
        if request.method == "OPTIONS":
            return make_response()
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        order = request.args.get('order', 'desc')
        
        service_id =  request.args.get('service', 1, type=int)
        notes = get_notes_service(service_id)
        
        notes_with_service_name = get_names_services(notes)
        
        total = len(notes_with_service_name)

        # Calcular el índice de inicio y final para la paginación
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page

        notes_data = notes_with_service_name[start_idx:end_idx]

        
        result = notes_schema.dump({'data': notes_data, 'page': page, 'per_page': per_page, 'total': total})
        
        return result, 200
    except Exception as e:
        return {"error": str(e)}, 401

@notes_api_bp.get("/me_notes_for_solicitude")
@jwt_required()
def list_me_notes_for_solicitude():
    """
    Lista las notas hechas de un usuario a un servicio en particular
    """

    try:
        if request.method == "OPTIONS":
            return make_response()
        
        solicitud_id =  request.args.get('solicitud_id', 1, type=int)
        user_id = get_jwt_identity()

        notes = get_me_notes_for_service(solicitud_id, user_id)

        notes_with_service_name = get_names_services(notes)
        
        total = len(notes_with_service_name)

        # Calcular el índice de inicio y final para la paginación

        notes_data = notes_with_service_name

        
        result = notes_schema.dump({'data': notes_data})
        
        return result, 200
    except Exception as e:
        return {"error": str(e)}, 401

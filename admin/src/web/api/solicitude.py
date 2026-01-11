from flask import Blueprint
from src.core.models.solicitude import Solicitude, Status, TypeService
from src.core.models.note import Note
from src.core.models.institutions import Institution
from src.core.models.users import User
from flask import session, jsonify, make_response, request
from src.web.schemas.solicitude import solicitude_schema, solicitudes_schema
from src.web.helpers.auth import login_required
from src.core.auth import find_user_by_email_and_pass
from src.core.models.users import User
from src.core.models.Institutional_Services.services import Service
from src.web.schemas.services import service_schema, services_schema
from src.web.helpers.auth import is_api_authenticated
from src.core.config.database import db
from flask_jwt_extended import jwt_required, get_jwt_identity

solicitude_api_bp = Blueprint("solicitude_api",__name__,url_prefix="/api/me/requests")

@solicitude_api_bp.get("/")
@jwt_required()
def list_solicitudes():
    if request.method == "OPTIONS":
        return make_response()
    if 'id' in request.args:
        return find_service_by_id()
        
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort = request.args.get('sort', 'inserted_at')
    order = request.args.get('order', 'desc')

    if order not in ['asc', 'desc']:
        order = 'desc'

    query = Solicitude.query.filter(Solicitude.user_id == user_id).order_by(db.desc(getattr(Solicitude, sort)))
    total = query.count()

    # Calcular el índice de inicio y final para la paginación
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page

    requests = query[start_idx:end_idx]
    
    result = solicitudes_schema.dump({'data': requests, 'page': page, 'per_page': per_page, 'total': total})

    return result, 200


@solicitude_api_bp.get("/listWithName")
@jwt_required()
def list_me_solicitudes_whit_name():
    try:
        if request.method == "OPTIONS":
            return make_response()

        user_id = get_jwt_identity()

        query = Solicitude.query.filter(Solicitude.user_id == user_id)
        
        lista= []
        
        for solicitud in query:
            id_service = solicitud.service_id
        
            service = Service.query.filter_by(id=id_service).first()
                        
            # Agregar el nombre de la institución a la lista
            lista.append({
                'service_id':service.id,
                'service_name': service.name,
                'id' :solicitud.id,
                'status': solicitud.status,
                'type_of_service':solicitud.type_of_service,
                'inserted_at' :solicitud.inserted_at,
            })
        
        result = solicitudes_schema.dump({'data': lista})

        return result, 200
    except Exception as e:
        return {"error": str(e)}, 401



@solicitude_api_bp.get("/list")
@jwt_required()
def list_me_solicitudes():
    try:
        if request.method == "OPTIONS":
            return make_response()

        user_id = get_jwt_identity()

        requests = Solicitude.query.filter(Solicitude.user_id == user_id)
        
        result = solicitudes_schema.dump({'data': requests})

        return result, 200
    except Exception as e:
        return {"error": str(e)}, 401




@solicitude_api_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def find_service_by_id():
    if request.method == "OPTIONS":
        return make_response()
    user_id = get_jwt_identity()
    id_service = request.args.get('id', type=int)
    if user_id and id_service:
        solicitude = Solicitude.query.filter_by(id=id_service, user_id=user_id).first()
        return jsonify(solicitude_schema.dump(solicitude)), 200
    return {"result": "Error, mandar email por id de header y id del servicio por uri."}, 401

@solicitude_api_bp.route('/', methods=['POST'])
@jwt_required()
def create_request():
    if request.method == "OPTIONS":
        return make_response()
    #user = find_user_by_email_and_pass(request.headers.get('Authorization'))
    json_data = request.get_json()

    if not json_data:
        return jsonify({'error': 'No se encontraron datos en el cuerpo de la solicitud'}), 400

    errors = solicitude_schema.validate(json_data)
    if errors:
        return jsonify({'error': 'Parámetros inválidos'}), 400
    
   #comment = json_data.get('comment')
    service_id = json_data.get('service_id')
    user_id = get_jwt_identity()
    type_of_service = json_data.get('type_of_service')
    status = Status.IN_PROCESS
    
    new_request = Solicitude(service_id=service_id, user_id=user_id, type_of_service=type_of_service, status=status)
    db.session.add(new_request)

    note = Note(
                user_id = user_id,
                solicitude_id = new_request.id,
                content = json_data.get('comment'))
    
    db.session.add(note)
    db.session.commit()

    return jsonify(solicitude_schema.dump(new_request)), 201

@solicitude_api_bp.route('/notes/', methods=['POST'])
@jwt_required()
def add_comment():
    if request.method == "OPTIONS":
        return make_response()
    
    print(request.args)
    id_request = request.args.get('id', type=int)
    json_data = request.get_json()
    user_id = get_jwt_identity()
    
    comment = '\n' + json_data.get('comment')
    solicitude = Solicitude.query.filter_by(id=id_request).first()
    
    note = Note(
        user_id = user_id,
        solicitude_id = solicitude.id,
        content = comment)
    db.session.add(note)
    db.session.commit()
    
    # return jsonify(solicitude_schema.dump(solicitude)), 201
    return {'data': "Nota creada"}, 201


@solicitude_api_bp.get("/finished")
@jwt_required()
def list_finished():
    query = Solicitude.query.filter(Solicitude.status == "FINISHED")
    
    lista = []  # Crear una lista vacía para almacenar los elementos
    
    for solicitud in query:
        id_service = solicitud.service_id
       
        id_institution = Service.query.filter_by(id=id_service).first().institutions_id
        
        name_institution = Institution.query.filter_by(id=id_institution).first().name
        
        # Agregar el nombre de la institución a la lista
        lista.append({
            'id': solicitud.id,
            'status': solicitud.status,
            'inserted_at':solicitud.inserted_at,
            'updated_at':solicitud.updated_at,
            'institution_name': name_institution,
        })
        
    print("Este es el request que devuelve la API", request)
    print(lista)
    result = solicitudes_schema.dump({'data': lista})

    return result, 200


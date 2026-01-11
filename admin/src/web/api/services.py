from os import abort
from flask import Blueprint
from src.core.models.Institutional_Services.services import Service
from src.core.models.institutions import Institution
from src.web.api.validations import validate_positive_int
from flask import session
from flask import jsonify
from src.web.schemas.services import service_schema, services_schema
from flask import request
from sqlalchemy import or_
from src.web.Filter_api.service_filter import filter



service_api_bp = Blueprint("service_api",__name__,url_prefix="/api/services")

@service_api_bp.get("/")
def index():
    try:
        validate_positive_int(request.args.get('id', -1, type=int))
        service_id = request.args.get('id', -1, type=int)
    except:
        return {"result": "Error, parametro id debe ser entero."}, 401
    if service_id == -1:
        return {"result": "Error, no se encontro ningun servicio con ese id."}, 401
    
  
    service = Service.query.filter_by(id=service_id).first()
    
    return jsonify(service_schema.dump(service)), 200

@service_api_bp.get("/List")
def ToltalList():
    services_data = Service.query.all()
    result = services_schema.dump({'data': services_data, 'total': len(services_data)})
    
    for service in result['data']:
        institution = Institution.query.get(service['institutions_id'])
        if institution:
            service['institution_name'] = institution.name
    
    return jsonify(result)
    

@service_api_bp.route("/search", methods=["GET"])
def List():
    
    try:
        name = request.args.get('name','') #Name
        q = request.args.get('q', '') #keyword
        type = request.args.get('type', '') #type_of_service 
        institution = request.args.get('institution', 0 , type=int) #institutions_id
        page = request.args.get('page', 1 ,type=int)
        per_page = request.args.get('per_page', None , type=int)
    
        flistros = {
            'name': name,
            'keyword': q,
            'type_of_service': type,
            'institution_id': institution,
        }
        
    except:
        return{"error": "Parámetros inválidos"}, 400
     
    
    
    services = filter(flistros)
    
    # Calcular el índice de inicio y final para la paginación
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    paginated_services = services[start_idx:end_idx]
    
    
    # Crear una respuesta JSON paginada
    services_data = services_schema.dump({'data': paginated_services, 'page': page, 'per_page': per_page, 'total': len(services)})
    
    for service in services_data['data']:
        institution = Institution.query.get(service['institutions_id'])
        if institution:
            service['institution_name'] = institution.name

    
    return jsonify(services_data), 200
    

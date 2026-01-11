from flask import Blueprint
from src.core.models.institutions import Institution
from flask import request
from flask import jsonify
from src.web.schemas.institutions import institution_schema, institutions_schema
from src.web.api.validations import validate_positive_int

institution_api_bp = Blueprint("institution_api",__name__,url_prefix="/api/institutions")

@institution_api_bp.get("/")
def index():

    # Obtener los parámetros de la URL
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 1, type=int)
        validate_positive_int(page, per_page)
    except:
        return {"error": "Parámetros inválidos"}, 400

    # Calcular el índice de inicio y final para la paginación
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page

    # Obtener las instituciones para la página actual
    institutions_data = Institution.query.all()
    paginated_institutions = institutions_data[start_idx:end_idx]

    # Serializar las instituciones utilizando Marshmallow
    result = institutions_schema.dump(paginated_institutions)

    # Crear una respuesta JSON paginada
    response = {
        "page": page,
        "per_page": per_page,
        "total": len(institutions_data),
        "data": result
    }

    return jsonify(response)


@institution_api_bp.get("/info")
def get_institution():
    
    institutions_id = int(request.args.get('id',-1))
    
    # Validar que la ID de la institución sea válida
    if not Institution.query.filter_by(id=institutions_id).first():
        return {"error": "ID de institución no válida"}, 404

    # Obtener información detallada de la institución
    institution = Institution.query.get(institutions_id)

    # Serializar la institución utilizando Marshmallow
    result = institution_schema.dump(institution)

    return jsonify(result)    

@institution_api_bp.get("/List")
def get_institutions():
    # Obtener todas las instituciones desde la base de datos
    institutions = Institution.query.all()

    # Serializar todas las instituciones utilizando Marshmallow
    result = institutions_schema.dump(institutions)

    return jsonify(result)
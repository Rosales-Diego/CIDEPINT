from flask import jsonify
from flask import Blueprint
from src.core.controller.errors import error_401
from flask import request
from src.web.schemas.services_types import services_type_schema
from src.core.models.Institutional_Services.services import Service

services_types_api_bp = Blueprint("services_type_api",__name__,url_prefix="/api/services-types")


@services_types_api_bp.get("/")
def index():
    valores_type_service = [tipo.value for tipo in Service.TypeService]
    data =   {
            "data": valores_type_service
            }
    return jsonify(data), 200
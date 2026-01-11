from flask import jsonify, make_response
from flask import Blueprint
from src.web.helpers.auth import find_user_by_id
from src.core.controller.errors import error_401
from flask import request
from src.core.auth import find_user_by_email_and_pass
from flask import session
from src.web.schemas.user import user_schema, users_schema
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request

user_api_bp = Blueprint("user_api",__name__,url_prefix="/api/me/profile/")

@user_api_bp.get("/")
@jwt_required()
def index():
    if request.method == "OPTIONS":
        return make_response()
    user_id = get_jwt_identity()
    user = find_user_by_id(user_id)
    if user:
        return jsonify(user_schema.dump(user)), 200
    else:
        return {"result": "No se encontro ningun usuario con ese email"}, 401
    
   
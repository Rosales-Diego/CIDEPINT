from flask import Blueprint, request, jsonify
from src.web.configs import config

contact_api_bp = Blueprint("contact_api",__name__,url_prefix="/api/contact")

@contact_api_bp.get('/')
def datos():
    contacto = config['inf_contacto']
    if contacto:
        return jsonify(contacto), 200
    else:
        return jsonify (contacto), 401
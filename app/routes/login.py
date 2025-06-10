from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token
from app.models.usuario_model import *
from datetime import timedelta


login_bp = Blueprint('login', __name__, url_prefix='/login')
@login_bp.route('/', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"success": False, "message": "Faltan credenciales"}), 400

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or not usuario.check_password(password):
        return jsonify({"success": False, "message": "Credenciales inválidas"}), 401

    access_token = create_access_token(identity=usuario.id, expires_delta=timedelta(hours=-3))

    return jsonify({
        "success": True,
        "message": "Inicio de sesión exitoso",
        "access_token": access_token
    }), 200
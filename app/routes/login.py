from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token
from app.models.usuario_model import Usuario
from datetime import timedelta
from flask_cors import cross_origin

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def login():
    if request.method == 'OPTIONS':
        # Responder al preflight request correctamente
        return '', 200

    # Manejar el POST para login
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"success": False, "message": "Faltan credenciales"}), 400

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or not usuario.check_password(password):
        return jsonify({"success": False, "message": "Credenciales inválidas"}), 401

    access_token = create_access_token(identity=str(usuario.id), 
                                       additional_claims={"rol": usuario.rol}, 
                                       expires_delta=timedelta(hours=1)
                                       )

    return jsonify({
        "success": True,
        "message": "Inicio de sesión exitoso",
        "access_token": access_token
    }), 200

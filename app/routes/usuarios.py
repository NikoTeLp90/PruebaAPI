from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from app.models.usuario_model import *
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

#Blueprint, todo lo que tenga prefijo usuarios_bp la ruta va a ser /usuarios
usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')




@usuarios_bp.route("/", methods = ['POST'])
@jwt_required()
def crear_usuario():
    claims = get_jwt()
    if claims['rol'] != 'admin':
        return jsonify({"msg": "No autorizado"}), 403
    
    data = request.get_json()
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    email = data.get('email')
    password = data.get('password')
    rol = data.get('rol')
  
    if not nombre or not email or not password:
        error_msg = "Faltan nombre, email o contraseña"

        return jsonify({'error': error_msg}), 400

    try:
        nuevo_usuario = Usuario(nombre=nombre,apellido=apellido,email=email,rol=rol)
        nuevo_usuario.set_password(password)
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return jsonify({
            'mensaje': 'Usuario creado con éxito',
            'usuario': {
                'id': nuevo_usuario.id,
                'nombre': nuevo_usuario.nombre,
                'apellido': nuevo_usuario.apellido,
                'email': nuevo_usuario.email,
                'rol': nuevo_usuario.rol
            }
        }), 201
    
    except SQLAlchemyError as e:
        db.session.rollback()
        error_msg = str(e)
        
    return jsonify({'error': error_msg}), 500
    

@usuarios_bp.route("/", methods = ['GET'])
@jwt_required()
def obtener_usuarios():
    claims = get_jwt()
    if claims['rol'] != 'admin':
        return jsonify({"msg": "No autorizado"}), 403
    
    try:
        q = request.args.get('q', '')
        usuarios = Usuario.query.all()

        if q:
            usuarios = [u for u in usuarios if q.lower() in u.nombre.lower()]

        usuarios_json = [{
            'id': u.id,
            'nombre': u.nombre,
            'apellido': u.apellido,
            'email': u.email,
            'rol': u.rol
        } for u in usuarios]

        return jsonify(usuarios_json), 200

    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

@usuarios_bp.route("/eliminar/<int:pk>", methods = ['POST'])
@jwt_required()
def eliminar_usuario(pk):
    claims = get_jwt()
    if claims['rol'] != 'admin':
        return jsonify({"msg": "No autorizado"}), 403
    
    try:
        usuario = Usuario.query.get_or_404(pk)
        db.session.delete(usuario)
        db.session.commit()
        

        return jsonify({'Mensaje':'Usuario eliminado con éxito'}),201
    
    except SQLAlchemyError as e:
        db.session.rollback()
        error_msg = str(e)
        
        return jsonify({"error":error_msg}), 500


@usuarios_bp.route("/editar/<int:pk>", methods=['POST'])
@jwt_required()
def editar_usuario(pk):
    
    claims = get_jwt()
    if claims['rol'] != 'admin':
        return jsonify({"msg": "No autorizado"}), 403
    
    usuario = Usuario.query.get_or_404(pk)

    data = request.get_json()
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    email = data.get('email')
    password = data.get('password')
    rol = data.get('rol')
   
    try:
        if nombre:
            usuario.nombre = nombre
        if apellido:
            usuario.apellido = apellido
        if email:
            usuario.email = email
        if password:
            usuario.set_password(password)
        if rol:
            usuario.rol = rol

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Usuario actualizado correctamente.",
            "usuario": {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "email": usuario.email,
                "rol": usuario.rol
            }
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
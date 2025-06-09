from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from app.models.usuario_model import *
from sqlalchemy.exc import SQLAlchemyError

#Blueprint, todo lo que tenga prefijo usuarios_bp la ruta va a ser /usuarios
usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')




@usuarios_bp.route("/", methods = ['POST'])
def crear_usuario():
    
    data = request.get_json()
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    email = data.get('email')
    password = data.get('password')
  
    if not nombre or not email or not password:
        error_msg = "Faltan nombre, email o contraseña"

        return jsonify({'error': error_msg}), 400

        
    
    try:
        nuevo_usuario = Usuario(nombre=nombre,apellido=apellido,email=email)
        nuevo_usuario.set_password(password)
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return jsonify({
            'mensaje': 'Usuario creado con éxito',
            'usuario': {
                'id': nuevo_usuario.id,
                'nombre': nuevo_usuario.nombre,
                'apellido': nuevo_usuario.apellido,
                'email': nuevo_usuario.email
            }
        }), 201
    
    except SQLAlchemyError as e:
        db.session.rollback()
        error_msg = str(e)
        
    return jsonify({'error': error_msg}), 500
    
    
@usuarios_bp.route("/", methods = ['GET'])
def obtener_usuarios():
    try:
        q = request.args.get('q', '')
        usuarios = Usuario.query.all()

        if q:
            usuarios = [u for u in usuarios if q.lower() in u.nombre.lower()]

        usuarios_json = [{
            'id': u.id,
            'nombre': u.nombre,
            'apellido': u.apellido,
            'email': u.email
        } for u in usuarios]

        return jsonify(usuarios_json), 200

    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

@usuarios_bp.route("/eliminar/<int:pk>", methods = ['POST'])
def eliminar_usuario(pk):
    
    try:
        usuario = Usuario.query.get_or_404(pk)
        db.session.delete(usuario)
        db.session.commit()
        
        if request.accept_mimetypes.accept_json:
            return jsonify({'Mensaje':'Usuario eliminado con éxito'}),201
        else:      
            return redirect(url_for('usuarios.obtener_usuarios'))
    
    except SQLAlchemyError as e:
        db.session.rollback()
        error_msg = str(e)
        
        if request.accept_mimetypes.accept_json:
            return jsonify({"error":error_msg}), 500
        else:
            return render_template("usuarios/lista_usuarios.html", error = error_msg)

@usuarios_bp.route("/editar/<int:pk>", methods=['POST'])
def editar_usuario(pk):
    usuario = Usuario.query.get_or_404(pk)

    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    email = request.form.get('email')
    password = request.form.get('password')

    if not nombre or not email:
        error_msg = "Nombre y email son obligatorios"
        
        return render_template("usuarios/editar_usuario.html", usuario=usuario, error=error_msg)
    
    try:
        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.email = email

        if password:
            usuario.set_password(password)

        db.session.commit()
        return redirect(url_for('usuarios.obtener_usuarios'))

    except SQLAlchemyError as e:
        db.session.rollback()
        error_msg = str(e)

        return render_template("usuarios/editar_usuario.html", usuario=usuario, error=error_msg)
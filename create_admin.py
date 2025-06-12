import sys
from app import create_app, db
from app.models.usuario_model import Usuario

app = create_app()
app.app_context().push()

def crear_admin(nombre, apellido, email, password, rol='admin'):
    if Usuario.query.filter_by(email=email).first():
        print(f"Ya existe un usuario con email {email}")
        return

    nuevo_usuario = Usuario(nombre=nombre, apellido=apellido, email=email, rol=rol)
    nuevo_usuario.set_password(password)
    db.session.add(nuevo_usuario)
    db.session.commit()
    print("Usuario admin creado con éxito.")

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Uso: python create_admin.py <nombre> <apellido> <email> <password>")
        sys.exit(1)

    nombre = sys.argv[1]
    apellido = sys.argv[2]
    email = sys.argv[3]
    password = sys.argv[4]

    crear_admin(nombre, apellido, email, password)
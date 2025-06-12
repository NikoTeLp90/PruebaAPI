from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.database import db

class Usuario(db.Model):
    
    #Se incluye si quisiera usar la remota y la local, habilitar desde __init__
    #__bind_key__ = "remota"  # Esto indica que usará la base remota
    
    __tablename__ = "usuarios"
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    pw_hash = db.Column(db.String(256), nullable = False)
    rol = db.Column(db.String(50), nullable = False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate = datetime.utcnow)
    
    
    def set_password(self,password):
        self.pw_hash = generate_password_hash(password)
        
    
    def check_password(self,password):
        return check_password_hash(self.pw_hash, password)
    
    
    def __repr__(self):
        return f'<Usuario {self.email}>'
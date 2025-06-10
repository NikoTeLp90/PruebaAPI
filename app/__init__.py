from flask import Flask
from .database import db
from .routes.usuarios import usuarios_bp
from .routes.login import login_bp
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import os

def create_app():
    app = Flask(__name__)

    
    ### -- Utilización de base local y base remota a la vez -- ###
    # Base principal (local)
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_local.sqlite'
    # app.config['SQLALCHEMY_BINDS'] = {
    #     'remota': 'postgresql://usuario:clave@host:puerto/dbname'  # reemplazá por tus datos reales
    # }
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    #SEGURIDAD DE LA APP
    app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
    
    jwt = JWTManager(app)
    
    
    #CREACION DE LA BASE, NO LA NECESITO SI USO REMOTA.
    #crear_base(app)
    
    #COMANDOS DE LA BASE
    CORS(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    
    
    #BLUEPRINTS, REGISTRAR LOS BLUEPRINTS
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(login_bp)
    
    return app
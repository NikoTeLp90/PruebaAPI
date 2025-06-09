from flask import Flask
from .database import crear_base, db
from .routes.usuarios import usuarios_bp
from flask_migrate import Migrate
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    ### -- Utilización de base local y base remota a la vez -- ###
    # Base principal (local)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_local.sqlite'
    # app.config['SQLALCHEMY_BINDS'] = {
    #     'remota': 'postgresql://usuario:clave@host:puerto/dbname'  # reemplazá por tus datos reales
    # }
    
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://neondb_owner:npg_AGwvm6R5OQMb@ep-square-art-a5xho0ns-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # crear_base(app)
    
    crear_base(app)
    migrate = Migrate(app, db)
    
    app.register_blueprint(usuarios_bp)
    
    return app
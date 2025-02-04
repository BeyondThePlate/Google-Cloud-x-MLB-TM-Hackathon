from flask import Flask,Blueprint
from flask_cors import CORS




def create_app():
    app = Flask(__name__)
    CORS(app)
    




    from backend_project_app.blueprints.ai.routes import aiRoute
    from backend_project_app.blueprints.db.routes import dbRoute
    from backend_project_app.blueprints.core.routes import core

    app.register_blueprint(core,url_prefix='/')
    app.register_blueprint(aiRoute,url_prefix='/ai')        
    app.register_blueprint(dbRoute,url_prefix='/db')


    
    return app
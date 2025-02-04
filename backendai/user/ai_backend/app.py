from flask import Flask,Blueprint
from flask_cors import CORS




def create_app():
    app = Flask(__name__)
    CORS(app)
    




    from ai_backend.blueprints.ai_backend.routes import aiBack
    from ai_backend.blueprints.core.routes import core


    app.register_blueprint(core,url_prefix='/')
    app.register_blueprint(aiBack,url_prefix='/aiback')        



    
    return app
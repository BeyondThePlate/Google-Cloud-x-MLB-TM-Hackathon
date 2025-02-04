# from flask import Flask
# from flask_cors import CORS
from backend_project_app.app import create_app


flask_app = create_app()


if __name__ == '__main__':
    flask_app.run(host="127.0.0.1", port=8080,debug=True)
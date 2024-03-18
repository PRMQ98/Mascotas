from flask import Flask
from flask_cors import CORS
from apilogin import login_blueprint

def create_app():
    app = Flask(__name__)
    CORS(app)  # Habilita CORS para todas las rutas
    app.register_blueprint(login_blueprint, url_prefix='/api')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=2024)

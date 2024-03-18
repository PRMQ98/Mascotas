from flask import Flask
from apilogin import login_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(login_blueprint, url_prefix='/api')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=2024)

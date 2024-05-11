from urllib.parse import unquote
from os import abort
from flask import Flask, jsonify, render_template, session
from flask_cors import CORS
from jinja2 import TemplateNotFound

app = Flask(__name__)
app.secret_key='Mascotas'
CORS(app)
CORS(app, resources={r"/mascotasimages/*": {"origins": "*"}})

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

@app.route('/crear_usuario')
def crear_usuario():
    return render_template('crear_usuario.html')

@app.route('/gestion-de-mascotas')
def gestion_de_mascotas():
    return render_template('gestion-de-mascotas.html')

@app.route('/gestion-de-formularios')
def gestion_de_formularios():
    return render_template('gestion-de-formularios.html')


@app.route('/actualizar-catalogo')
def actualizar_catalogo():
    return render_template('actualizar-catalogo.html')

@app.route('/ver-catalogo')
def ver_catalogo():
    return render_template('ver-catalogo.html')

@app.route('/vista-de-formularios')
def vista_formularios():
    return render_template('vista-de-formularios.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None) 
    return jsonify({'message': 'Logged out successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True, port=2025)

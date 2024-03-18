from flask import Blueprint, request, jsonify
import pyodbc
import json

# Cargar configuración de la base de datos
with open('db_config.json') as config_file:
    db_config = json.load(config_file)

# Cadena de conexión
conn_str = f"DRIVER={db_config['driver']};SERVER={db_config['server']};DATABASE={db_config['database']};UID={db_config['username']};PWD={db_config['password']}"

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']  # En un caso real, esta contraseña debería ser un hash

    try:
        # Intento de conexión a la base de datos
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        print("Conexión a la base de datos exitosa")  # Mensaje en consola para el desarrollador
    except Exception as e:
        return jsonify({"error": "No se pudo conectar a la base de datos", "message": str(e)}), 500

    # Verificar el usuario y la contraseña
    query = "SELECT * FROM Users WHERE Username = ? AND Password = ?"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    if user:
        return jsonify({"message": "Login exitoso", "username": username}), 200
    else:
        return jsonify({"message": "Usuario o contraseña incorrectos"}), 401
    

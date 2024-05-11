from genericpath import isfile
from ntpath import join
from flask import Flask, request, jsonify, send_from_directory, url_for
from flask import send_file
from flask_cors import CORS
import apilogin, apimascotas
import os

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/mascotasimages/*": {"origins": "*"}})

menus_por_rol = {
    "MSALUD": ["Inicio", "Agregar Mascotas", "Gestión de Formularios"],
    "DSALUD": ["Inicio", "Vista de Formularios", "Actualizar Catálogo"],
    "UFinal": ["Inicio", "Ver catálogo"]
}

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user_info = apilogin.get_user_info(data.get('username'), data.get('password'))
    if user_info:
        return jsonify({
            "message": "Login successful",
            "user": user_info,
            "menus": menus_por_rol.get(user_info["rol"], [])
        }), 200
    return jsonify({"message": "Invalid credentials"}), 401


@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    data = request.json
    try:
        apilogin.crear_usuario(
            nombres=data['nombres'], 
            apellidos=data['apellidos'], 
            dpi=data['dpi'], 
            direccion=data['direccion'], 
            numeroTelefono=data['numeroTelefono'], 
            correoElectronico=data['correoElectronico']
        )
        return jsonify({"mensaje": "Usuario creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

UPLOAD_FOLDER = 'C:/Users/PaMoq/Desktop/mascotasimages'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def guardar_imagen(imagen):
    if not imagen or imagen.filename == '':
        return None
    if not allowed_file(imagen.filename):
        raise ValueError('Tipo de archivo no permitido')
    imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], imagen.filename)
    imagen.save(imagen_path)
    return imagen.filename  # Devuelve solo el nombre del archivo

@app.route('/mascotasimages/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/mascotas', methods=['POST'])
def crear_mascota():
    print("Recibiendo datos del formulario")
    tipo = request.form.get('tipo')
    nombre = request.form.get('nombre')
    raza = request.form.get('raza')
    edad = request.form.get('edad')
    fotografia = request.files.get('fotografia')
    if fotografia:
        fotografia_url = guardar_imagen(fotografia)
        if fotografia_url and not fotografia_url.startswith('/'):
            fotografia_url = '/' + fotografia_url
    else:
        fotografia_url = None
    print(f"Datos recibidos: {tipo}, {nombre}, {raza}, {edad}, {fotografia_url}")

    try:
        apimascotas.crear_mascota(tipo, nombre, raza, edad, fotografia_url)
        print("Mascota creada exitosamente")
        return jsonify({"mensaje": "Mascota creada exitosamente"}), 201
    except Exception as e:
        print("Error al crear mascota:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/mascotas', methods=['GET'])
def listar_mascotas():
    try:
        mascotas = apimascotas.obtener_mascotas()
        for mascota in mascotas:
            if mascota['FotografiaURL'] and not mascota['FotografiaURL'].startswith('http'):
                mascota['FotografiaURL'] = url_for('uploaded_file', filename=mascota['FotografiaURL'])
        return jsonify(mascotas), 200
    except Exception as e:
        print("Error interno del servidor al listar mascotas:", e)
        return jsonify({"error": "Error interno del servidor"}), 500


@app.route('/mascotas/<int:mascota_id>', methods=['GET'])
def mostrar_mascota(mascota_id):
    try:
        mascota = apimascotas.obtener_mascota_por_id(mascota_id)
        if mascota:
            return jsonify(mascota), 200
        else:
            return jsonify({"mensaje": "Mascota no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    

@app.route('/mascotas/publicar/<int:mascota_id>', methods=['POST'])
def publicar_mascota(mascota_id):
    print("Endpoint alcanzado con ID:", mascota_id)
    resultado = apimascotas.publicar_mascota(mascota_id)
    if resultado:
        return jsonify({"mensaje": "Mascota publicada exitosamente"}), 200
    else:
        return jsonify({"mensaje": "Mascota no encontrada"}), 404
    

@app.route('/mascotas/disponibles', methods=['GET'])
def listar_mascotas_disponibles():
    try:
        mascotas = apimascotas.obtener_mascotas_disponibles()  
        return jsonify(mascotas), 200
    except Exception as e:
        print("Error interno del servidor al listar mascotas disponibles:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/mascotas/adoptar/<int:mascota_id>', methods=['POST'])
def adoptar_mascota_route(mascota_id):
    data = request.get_json()
    usuario_id = data['usuarioId'] 
    resultado = apimascotas.adoptar_mascota(mascota_id, usuario_id)
    if resultado:
        return jsonify({"mensaje": "Mascota adoptada exitosamente"}), 200
    else:
        return jsonify({"mensaje": "Mascota no encontrada"}), 404

@app.route('/imagenesinicio/<filename>')
def send_images(filename):
    return send_from_directory('C:/Users/PaMoq/Desktop/mascotasimages/imagenesinicio', filename)

def obtener_lista_imagenes():
    directorio = 'C:/Users/PaMoq/Desktop/mascotasimages/imagenesinicio'
    imagenes = [f for f in os.listdir(directorio) if isfile(join(directorio, f))]
    return imagenes

@app.route('/imagenesinicio', methods=['GET'])
def obtener_imagenes_inicio():
    try:
        imagenes = obtener_lista_imagenes()
        return jsonify(imagenes), 200
    except Exception as e:
        print("Error interno del servidor al obtener imágenes:", e)
        return jsonify({"error": "Error interno del servidor"}), 500


@app.route('/mascotas/adoptadas', methods=['GET'])
def get_mascotas_adoptadas():
    mascotas_adoptadas = apimascotas.listar_mascotas_adoptadas()
    if mascotas_adoptadas:
        return jsonify(mascotas_adoptadas), 200
    else:
        return jsonify({"mensaje": "No se encontraron mascotas adoptadas"}), 404

@app.route('/descargar_pdf_mascota/<int:mascota_id>', methods=['GET'])
def descargar_pdf_mascota(mascota_id):
    path_to_pdf = apimascotas.generar_pdf_mascota(mascota_id)
    print("Path to PDF:", path_to_pdf) 
    if path_to_pdf and os.path.exists(path_to_pdf):
        try:
            return send_file(path_to_pdf, as_attachment=False)
        except Exception as e:
            print(f"Error al enviar el archivo: {e}")
            return "Error al enviar el archivo", 500
    else:
        return "No se encontró la mascota o no se pudo generar el PDF", 404


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, port=2024)

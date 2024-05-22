import db

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def crear_mascota(tipo, nombre, raza, edad, fotografia_url):
    try:
        with db.get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO DBAMASCOTAS.Mascotas (Tipo, Nombre, Raza, Edad, FotografiaURL)
                    VALUES (?, ?, ?, ?, ?)
                """, (tipo, nombre, raza, edad, fotografia_url))
                conn.commit()
    except Exception as e:
        print("Error al crear la mascota:", e)
        raise

def obtener_mascotas():
    with db.get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT MascotaID, Tipo, Nombre, Raza, Edad, Estado, FotografiaURL FROM DBAMASCOTAS.Mascotas")
            mascotas = cursor.fetchall()
            columnas = [column[0] for column in cursor.description]
            return [dict(zip(columnas, fila)) for fila in mascotas]


def obtener_mascota_por_id(mascota_id):
    with db.get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT MascotaID, Tipo, Nombre, Raza, Edad, FotografiaURL FROM DBAMASCOTAS.Mascotas WHERE MascotaID = ?", (mascota_id,))
            return cursor.fetchone()


def publicar_mascota(mascota_id):
    conn = db.get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE DBAMASCOTAS.Mascotas
            SET Estado = 'Disponible'
            WHERE MascotaID = ?
        """, (mascota_id,))
        if cursor.rowcount == 0:
            return False  
        conn.commit()
        return True  
    except Exception as e:
        print("Error al publicar la mascota:", e)
        conn.rollback()
        return False  
    finally:
        conn.close()

def obtener_mascotas_disponibles():
    with db.get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT MascotaID, Tipo, Nombre, Raza, Edad, FotografiaURL FROM DBAMASCOTAS.Mascotas WHERE Estado = 'Disponible'")
            mascotas = cursor.fetchall()
            columnas = [column[0] for column in cursor.description]
            return [dict(zip(columnas, fila)) for fila in mascotas]
        

def adoptar_mascota(mascota_id, usuario_id):
    conn = db.get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE DBAMASCOTAS.Mascotas
            SET Estado = 'Adoptado', UsuarioID = ?
            WHERE MascotaID = ?
        """, (usuario_id, mascota_id))
        if cursor.rowcount == 0:
            return False  
        conn.commit()
        return True  
    except Exception as e:
        print("Error al adoptar la mascota:", e)
        conn.rollback()
        return False  
    finally:
        conn.close()


def listar_mascotas_adoptadas():
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                M.MascotaID,
                M.Tipo,
                M.Nombre,
                M.Raza,
                M.Edad,
                M.Estado,
                M.FotografiaURL,
                U.UsuarioID,
                U.Nombres,
                U.Apellidos,
                U.DPI,
                U.Direccion,
                U.NumeroTelefono,
                U.CorreoElectronico,
                R.Nombre AS RolNombre
            FROM
                DBAMASCOTAS.Mascotas M
            INNER JOIN
                DBAMASCOTAS.Usuarios U ON M.UsuarioID = U.UsuarioID
            INNER JOIN
                DBAMASCOTAS.Roles R ON U.RolID = R.RolID
            WHERE
                M.Estado = 'Adoptado'
        """)
        mascotas = cursor.fetchall()
        columnas = [column[0] for column in cursor.description]
        resultado = [dict(zip(columnas, fila)) for fila in mascotas]
        conn.close()
        return resultado
    except Exception as e:
        print("Error al listar mascotas adoptadas:", e)
        return []


def generar_pdf_mascota(mascota_id):
    conn = db.get_db_connection() 
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT M.MascotaID, M.Tipo, M.Nombre, M.Raza, M.Edad,
                   U.Nombres, U.Apellidos, U.CorreoElectronico, U.NumeroTelefono
            FROM DBAMASCOTAS.Mascotas M
            JOIN DBAMASCOTAS.Usuarios U ON M.UsuarioID = U.UsuarioID
            WHERE M.MascotaID = ? AND M.Estado = 'Adoptado'
        """, (mascota_id,))
        mascota = cursor.fetchone()
        if mascota:
            filename = f'mascotas_adoptadas_{mascota_id}.pdf'
            return generar_pdf_detalle(filename, mascota)
        else:
            return None
    except Exception as e:
        print(f"Error al generar PDF para mascota {mascota_id}: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def generar_pdf_detalle(filename, mascota):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    c = canvas.Canvas(filename, pagesize=letter)
    y = 750  # Inicio en la parte superior del documento

    # Crear el contenido del PDF
    details = [
        f"Nombre de la mascota: {mascota[2]}",
        f"Tipo: {mascota[1]}",
        f"Raza: {mascota[3]}",
        f"Edad: {mascota[4]} meses",
        f"Adoptante: {mascota[5]} {mascota[6]}",
        f"Correo Electrónico: {mascota[7]}",
        f"Teléfono: {mascota[8]}"
    ]

    for detail in details:
        c.drawString(72, y, detail)
        y -= 40  

    c.save()
    return filename


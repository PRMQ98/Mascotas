import db

def get_user_info(email, dpi):
    with db.get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT U.UsuarioID, U.Nombres, U.Apellidos, U.CorreoElectronico, R.Nombre AS RolNombre
                FROM DBAMASCOTAS.Usuarios U
                INNER JOIN DBAMASCOTAS.Roles R ON U.RolID = R.RolID
                WHERE U.CorreoElectronico = ? AND U.DPI = ?
            """, (email, dpi))
            user_info = cursor.fetchone()
            if user_info:
                return {
                    "UsuarioID": user_info.UsuarioID,
                    "nombres": user_info.Nombres,
                    "apellidos": user_info.Apellidos,
                    "correoElectronico": user_info.CorreoElectronico,
                    "rol": user_info.RolNombre
                }
    return None

def crear_usuario(nombres, apellidos, dpi, direccion, numeroTelefono, correoElectronico):
    try:
        with db.get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT RolID FROM DBAMASCOTAS.Roles WHERE Nombre = 'UFinal'")
                rol_id = cursor.fetchone()[0]

                cursor.execute("""
                    INSERT INTO DBAMASCOTAS.Usuarios 
                    (Nombres, Apellidos, DPI, Direccion, NumeroTelefono, CorreoElectronico, RolID)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (nombres, apellidos, dpi, direccion, numeroTelefono, correoElectronico, rol_id))
                conn.commit()
    except Exception as e:
        print("Error al crear el usuario:", e)
        raise

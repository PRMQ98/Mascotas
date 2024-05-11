-- 1. Crear la Base de Datos MASCOTAS
CREATE DATABASE MASCOTAS;
GO

-- Cambiar al contexto de la base de datos MASCOTAS
USE MASCOTAS;
GO

-- 2. Crear el Esquema DBAMASCOTAS
CREATE SCHEMA DBAMASCOTAS AUTHORIZATION dbo;
GO

-- Cambiar al contexto de la base de datos master para crear el login
USE master;
GO

-- 3. Crear un Nuevo Login para el Servidor
CREATE LOGIN DBAMASCOTAS WITH PASSWORD = 'DBA1998';
GO

-- Cambiar de nuevo al contexto de la base de datos MASCOTAS
USE MASCOTAS;
GO

-- 4. Crear un Usuario de Base de Datos para el Login Creado Previo
CREATE USER DBAMASCOTAS FOR LOGIN DBAMASCOTAS WITH DEFAULT_SCHEMA = DBAMASCOTAS;
GO

-- Opcional: Asignar roles o permisos específicos al usuario
ALTER ROLE db_owner ADD MEMBER DBAMASCOTAS;
GO

-- 5. Crear las Tablas Dentro del Esquema DBAMASCOTAS
CREATE TABLE DBAMASCOTAS.Roles (
    RolID INT PRIMARY KEY IDENTITY(1,1),
    Nombre NVARCHAR(50) NOT NULL
);
GO

CREATE TABLE DBAMASCOTAS.Usuarios (
    UsuarioID INT PRIMARY KEY IDENTITY(1,1),
    Nombres NVARCHAR(100),
    Apellidos NVARCHAR(100),
    DPI NVARCHAR(20) UNIQUE,
    Direccion NVARCHAR(255),
    NumeroTelefono NVARCHAR(20),
    CorreoElectronico NVARCHAR(100),
    RolID INT,
    FOREIGN KEY (RolID) REFERENCES DBAMASCOTAS.Roles(RolID)
);
GO

CREATE TABLE DBAMASCOTAS.Mascotas (
    MascotaID INT PRIMARY KEY IDENTITY(1,1),
    Tipo NVARCHAR(50),
    Nombre NVARCHAR(100),
    Raza NVARCHAR(100),
    Edad INT,
    Fotografia VARBINARY(MAX)
);
GO


CREATE TABLE DBAMASCOTAS.Formularios (
    FormularioID INT PRIMARY KEY IDENTITY(1,1),
    UsuarioID INT,
    MascotaID INT,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (UsuarioID) REFERENCES DBAMASCOTAS.Usuarios(UsuarioID),
    FOREIGN KEY (MascotaID) REFERENCES DBAMASCOTAS.Mascotas(MascotaID)
);
GO

CREATE TABLE DBAMASCOTAS.FechasCastracion (
    FechaCastracionID INT PRIMARY KEY IDENTITY(1,1),
    Fecha DATETIME,
    MascotaID INT,
    FOREIGN KEY (MascotaID) REFERENCES DBAMASCOTAS.Mascotas(MascotaID)
);
GO

-- Crear una tabla simplificada para almacenar información sobre las imágenes
CREATE TABLE DBAMASCOTAS.ImagenesFrontend (
    ID_Imagen INT PRIMARY KEY IDENTITY(1,1),
    Nombre NVARCHAR(255) NOT NULL,
    FotografiaURL NVARCHAR(MAX) NOT NULL
);
GO

ALTER TABLE DBAMASCOTAS.Mascotas
DROP COLUMN Fotografia; -- Eliminar la columna existente

ALTER TABLE DBAMASCOTAS.Mascotas
ADD FotografiaURL NVARCHAR(MAX); -- Agregar una nueva columna para la URL de la imagen

ALTER LOGIN DBAMASCOTAS WITH DEFAULT_DATABASE = MASCOTAS;

ALTER TABLE DBAMASCOTAS.Mascotas
ADD Estado NVARCHAR(50) DEFAULT 'No Disponible';
GO


ALTER TABLE DBAMASCOTAS.Mascotas
ADD UsuarioID INT NULL,
    CONSTRAINT FK_Mascotas_Usuarios FOREIGN KEY (UsuarioID)
    REFERENCES DBAMASCOTAS.Usuarios (UsuarioID);
GO

---listar todas las mascotas adoptadas
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
    M.Estado = 'Adoptado';  -- Filtra para mostrar solo las mascotas que han sido adoptadas


SELECT * FROM DBAMASCOTAS.Usuarios;

SELECT @@SERVERNAME AS 'ServerName'

SELECT * FROM DBAMASCOTAS.ImagenesFrontend

SELECT U.*
FROM DBAMASCOTAS.Usuarios U
INNER JOIN DBAMASCOTAS.Roles R ON U.RolID = R.RolID
WHERE R.Nombre = 'MSALUD';

UPDATE DBAMASCOTAS.Mascotas
SET UsuarioID = NULL
WHERE UsuarioID IS NOT NULL;

UPDATE DBAMASCOTAS.Mascotas
SET Estado = 'No Disponible'
WHERE Estado = 'Adoptado';
GO

DELETE FROM DBAMASCOTAS.Mascotas WHERE MascotaID = '23';

INSERT INTO DBAMASCOTAS.ImagenesFrontend (Nombre, FotografiaURL)
VALUES 
('castracion', 'http://localhost:2024/imagenesinicio/castracion.jpg'),
('informacion', 'http://localhost:2024/imagenesinicio/informacion.jpg'),
('vacunacion', 'http://localhost:2024/imagenesinicio/vacunacion.jpg'),
('departamentales', 'http://localhost:2024/imagenesinicio/departamentales.jpg');
GO

INSERT INTO DBAMASCOTAS.Mascotas (Tipo, Nombre, Raza, Edad, FotografiaURL)
VALUES ('Perro', 'Fido', 'Labrador', 3, 'https://drive.google.com/file/d/113PoLrX3TYSrgKZt84kCef8OyKdX64nG/view?usp=drive_link');

-- Insertar roles iniciales
INSERT INTO DBAMASCOTAS.Roles (Nombre) VALUES ('MSALUD'), ('DSALUD'), ('UFinal');
GO


-- Insertar un usuario para el rol MSALUD
INSERT INTO DBAMASCOTAS.Usuarios (Nombres, Apellidos, DPI, Direccion, NumeroTelefono, CorreoElectronico, RolID)
VALUES ('Pablo', 'Morales', '2965298930313', '5ta avenida 3-13', '22445588', 'patito.yo95@gmail.com', (SELECT RolID FROM DBAMASCOTAS.Roles WHERE Nombre = 'MSALUD'));

-- Insertar un usuario para el rol DSALUD
INSERT INTO DBAMASCOTAS.Usuarios (Nombres, Apellidos, DPI, Direccion, NumeroTelefono, CorreoElectronico, RolID)
VALUES ('Emmanuel', 'Ajsivinac', '2865298930313', '5ta avenida 3-13', '22445589', 'patito.yo95@gmail.com', (SELECT RolID FROM DBAMASCOTAS.Roles WHERE Nombre = 'DSALUD'));

-- Insertar un usuario para el rol UFinal
INSERT INTO DBAMASCOTAS.Usuarios (Nombres, Apellidos, DPI, Direccion, NumeroTelefono, CorreoElectronico, RolID)
VALUES ('Brenda', 'Pérez', '2765298930313', '5ta avenida 3-13', '22445590', 'patito.yo95@gmail.com', (SELECT RolID FROM DBAMASCOTAS.Roles WHERE Nombre = 'UFinal'));

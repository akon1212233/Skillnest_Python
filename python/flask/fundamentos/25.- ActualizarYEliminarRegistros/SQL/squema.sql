- ==========================================================
-- CREAR BASE DE DATOS
-- ==========================================================

CREATE DATABASE IF NOT EXISTS esquema_estudiantes;

USE esquema_estudiantes;


-- ==========================================================
-- CREAR TABLA
-- ==========================================================

CREATE TABLE IF NOT EXISTS estudiantes (

    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,

    nombre VARCHAR(100),

    email VARCHAR(100),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);


-- ==========================================================
-- INSERTAR DATOS DE PRUEBA
-- ==========================================================

INSERT INTO estudiantes
(
    nombre,
    email
)
VALUES
(
    "Joe Doe",
    "joedoe@email.com"
),
(
    "Ana Pérez",
    "ana@email.com"
),
(
    "Carlos Soto",
    "carlos@email.com"
),
(
    "María González",
    "maria@email.com"
);
-- ==========================================================
-- BASE DE DATOS
-- ==========================================================

CREATE DATABASE IF NOT EXISTS esquema_usuarios;

USE esquema_usuarios;


-- ==========================================================
-- TABLA USUARIOS
-- ==========================================================

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);


-- ==========================================================
-- DATOS DE PRUEBA
-- ==========================================================

INSERT INTO usuarios
(
    nombre,
    apellido,
    email
)
VALUES
(
    "Soraya",
    "Montenegro",
    "soraya@email.com"
),
(
    "Armando",
    "Mendoza",
    "armando@email.com"
),
(
    "Mia",
    "Colucci",
    "mia@email.com"
),
(
    "Rubi",
    "Perez",
    "rubi@email.com"
);

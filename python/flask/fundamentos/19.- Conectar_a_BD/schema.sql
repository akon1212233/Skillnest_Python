-- ==========================================================
-- CREAR BASE DE DATOS
-- ==========================================================

CREATE DATABASE IF NOT EXISTS primera_flask;

USE primera_flask;


-- ==========================================================
-- CREAR TABLA
-- ==========================================================

CREATE TABLE IF NOT EXISTS mascotas (

    id INT AUTO_INCREMENT PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL,

    tipo VARCHAR(100) NOT NULL,

    color VARCHAR(100) NOT NULL,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP

);


-- ==========================================================
-- INSERTAR DATOS DE PRUEBA
-- ==========================================================

INSERT INTO mascotas
    (nombre, tipo, color)
VALUES
    ("Firulais", "Perro", "Café"),
    ("Michi", "Gato", "Negro"),
    ("Luna", "Perro", "Blanco"),
    ("Nala", "Gato", "Naranjo"),
    ("Coco", "Conejo", "Blanco");


CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    edad INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO usuarios
    (nombre, email, edad)
VALUES
    ("Akon","akon12123@gmail.com","18"),
    ("Mauricio","mauriperro48@gmail.com","90"),
    ("Marcelo","Marcelon41@gmail.com","17"),
    ("Daniel","danieljimenez@liceovvh.cl","16"),
    ("Juan","xXJuanPrevalsXx@gmail.com","18"),
    ("Kevin","KVN199@gmail.com","21"),
    ("Jheimy","jsl1d3k2jn@gmail.com","17");
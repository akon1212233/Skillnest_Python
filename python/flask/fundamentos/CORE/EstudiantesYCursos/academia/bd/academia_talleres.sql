-- ==========================================================
-- CREACIÓN DE LA BASE DE DATOS
-- ==========================================================

CREATE DATABASE IF NOT EXISTS academia_talleres;

USE academia_talleres;


-- ==========================================================
-- TABLA TALLERES
-- ==========================================================

CREATE TABLE IF NOT EXISTS talleres (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(60) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);


-- ==========================================================
-- TABLA ALUMNOS
-- ==========================================================

CREATE TABLE IF NOT EXISTS alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(45) NOT NULL,
    apellido VARCHAR(45) NOT NULL,
    edad INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    taller_id INT NOT NULL,

    CONSTRAINT fk_alumnos_taller
        FOREIGN KEY (taller_id)
        REFERENCES talleres(id)
);


-- ==========================================================
-- DATOS DE PRUEBA
-- ==========================================================

INSERT INTO talleres (titulo) VALUES
("Robótica"),
("Fotografía"),
("Python"),
("Diseño Web");

INSERT INTO alumnos (nombre, apellido, edad, taller_id) VALUES
("Camila",   "Vargas",   19, 1),
("Joaquín",  "Riquelme", 21, 1),
("Fernanda", "Lagos",    20, 1),
("Tomás",    "Araya",    22, 1),
("Isidora",  "Muñoz",    18, 2),
("Benjamín", "Rojas",    23, 3);

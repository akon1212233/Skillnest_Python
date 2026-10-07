-- ==========================================================
-- CREAR BASE DE DATOS
-- ==========================================================

CREATE DATABASE IF NOT EXISTS esquema_tacos;

USE esquema_tacos;


-- ==========================================================
-- TABLA RESTAURANTES
-- ==========================================================

CREATE TABLE IF NOT EXISTS restaurantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(45) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);


-- ==========================================================
-- TABLA TACOS
-- ==========================================================

CREATE TABLE IF NOT EXISTS tacos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tortilla VARCHAR(45),
    guiso VARCHAR(45),
    salsa VARCHAR(45),
    restaurante_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_tacos_restaurantes
        FOREIGN KEY (restaurante_id)
        REFERENCES restaurantes(id)
);


-- ==========================================================
-- RESTAURANTES DE PRUEBA
-- ==========================================================

INSERT INTO restaurantes
(nombre)
VALUES
("Tacos El Sol"),
("Tacos Central"),
("Tacos Don Pepe");


-- ==========================================================
-- TACOS DE PRUEBA
-- ==========================================================

INSERT INTO tacos
(
    tortilla,
    guiso,
    salsa,
    restaurante_id
)
VALUES
(
    "Maíz",
    "Carne",
    "Verde",
    1
),
(
    "Harina",
    "Pollo",
    "Roja",
    1
),
(
    "Maíz",
    "Carnitas",
    "Verde",
    2
),
(
    "Maíz",
    "Pastor",
    "Picante",
    2
),
(
    "Harina",
    "Barbacoa",
    "Roja",
    3
);
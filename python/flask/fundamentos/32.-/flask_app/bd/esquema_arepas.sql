-- ==========================================================
-- BASE DE DATOS
-- ==========================================================

CREATE DATABASE IF NOT EXISTS esquema_arepas;

USE esquema_arepas;


-- ==========================================================
-- TABLA PEDIDOS
-- ==========================================================

CREATE TABLE IF NOT EXISTS pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo_arepa VARCHAR(100) NOT NULL,
    cantidad INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);


-- ==========================================================
-- DATOS DE PRUEBA
-- ==========================================================

INSERT INTO pedidos
(
    nombre,
    tipo_arepa,
    cantidad
)
VALUES
(
    "María",
    "Arepa de queso",
    2
),
(
    "Carlos",
    "Arepa de carne",
    3
),
(
    "Ana",
    "Arepa de pollo",
    1
);

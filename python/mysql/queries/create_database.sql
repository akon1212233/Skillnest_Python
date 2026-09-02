-- Script MySQL para crear la base de datos del sistema de usuarios y mensajes
CREATE DATABASE IF NOT EXISTS skillnest_users;
USE skillnest_users;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    tipo_usuario ENUM('Administrador', 'Usuario') NOT NULL DEFAULT 'Usuario',
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mensajes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    contenido TEXT NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS comentarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mensaje_id INT NOT NULL,
    usuario_id INT NOT NULL,
    contenido TEXT NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (mensaje_id) REFERENCES mensajes(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

INSERT INTO usuarios (nombre, email, contrasena, tipo_usuario)
VALUES
    ('Patricia', 'patricia@codingdojo.com', 'admin123', 'Administrador'),
    ('Andrea', 'andrea@codingdojo.com', 'user123', 'Usuario'),
    ('Katya', 'katya@codingdojo.com', 'user123', 'Usuario');

INSERT INTO mensajes (usuario_id, contenido)
VALUES
    (2, 'Mensaje de ejemplo para Andrea.');

INSERT INTO comentarios (mensaje_id, usuario_id, contenido)
VALUES
    (1, 1, 'Comentario de Patricia.');

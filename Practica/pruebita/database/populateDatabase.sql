USE usuarios_db;
INSERT INTO tipoUsuario (idTipoUsuario, nombreTipoUsuario) VALUES (1, 'Administrador'), (2, 'Usuario');
INSERT INTO usuario (idTipoUsuario, nombreUsuario, emailUsuario, contrasenaUsuario)
VALUES (1, 'Administrador', 'admin@example.com', 'admin123');
INSERT INTO usuario (idTipoUsuario, nombreUsuario, emailUsuario, contrasenaUsuario)
VALUES (2, 'Usuario', 'user@example.com', 'user123');
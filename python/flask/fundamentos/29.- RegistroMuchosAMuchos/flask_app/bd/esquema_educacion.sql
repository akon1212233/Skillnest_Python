-- ==========================================================
-- CREAR BASE DE DATOS
-- ==========================================================

CREATE DATABASE IF NOT EXISTS esquema_educacion;

USE esquema_educacion;


-- ==========================================================
-- TABLA ESTUDIANTES
-- ==========================================================

CREATE TABLE IF NOT EXISTS estudiantes (
    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ==========================================================
-- TABLA CURSOS
-- ==========================================================

CREATE TABLE IF NOT EXISTS cursos (
    id_curso INT AUTO_INCREMENT PRIMARY KEY,
    nombre_curso VARCHAR(100) NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ==========================================================
-- TABLA INTERMEDIA
-- ==========================================================

CREATE TABLE IF NOT EXISTS inscripciones (
    estudiante_id INT NOT NULL,
    curso_id INT NOT NULL,

    PRIMARY KEY (
        estudiante_id,
        curso_id
    ),

    CONSTRAINT fk_inscripcion_estudiante
        FOREIGN KEY (estudiante_id)
        REFERENCES estudiantes(id_estudiante),

    CONSTRAINT fk_inscripcion_curso
        FOREIGN KEY (curso_id)
        REFERENCES cursos(id_curso)
);


-- ==========================================================
-- ESTUDIANTES DE PRUEBA
-- ==========================================================

INSERT INTO estudiantes
(
    nombre,
    email
)
VALUES
(
    "Juan Pérez",
    "juan@email.com"
),
(
    "Ana González",
    "ana@email.com"
),
(
    "Carlos Soto",
    "carlos@email.com"
),
(
    "María López",
    "maria@email.com"
);


-- ==========================================================
-- CURSOS DE PRUEBA
-- ==========================================================

INSERT INTO cursos
(
    nombre_curso,
    descripcion
)
VALUES
(
    "MERN",
    "Desarrollo web con MongoDB, Express, React y Node.js"
),
(
    "Python",
    "Programación y desarrollo web con Python"
),
(
    "Java",
    "Desarrollo de aplicaciones utilizando Java"
),
(
    "Fundamentos de la Web",
    "HTML, CSS y conceptos fundamentales de desarrollo web"
);
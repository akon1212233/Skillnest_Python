# BookHub — Simulación de Certificación FullStack Python/Flask

Aplicación web desarrollada con Flask, MySQL, PyMySQL, Jinja2, Bootstrap y arquitectura MVC modularizada.

## Funcionalidades

- Registro de usuarios con Bcrypt.
- Inicio y cierre de sesión mediante sesiones Flask.
- Validaciones backend y mensajes flash.
- CRUD completo de libros.
- Control de propiedad: un usuario solo puede editar/eliminar sus propios libros.
- Exploración de libros publicados por toda la comunidad.
- Vista de detalle de cada libro.
- Agregar/quitar libros de favoritos.
- Vista de libros favoritos.
- Relaciones MySQL entre usuarios, libros y favoritos.
- ERD en `resources/ERD.svg`.
- Configuración mediante `.env` y dependencias en `requirements.txt`.

## Instalación

### 1. Crear entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate
```

En Windows:

```powershell
.venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Crear la base de datos

Asegúrate de tener MySQL/MariaDB iniciado y ejecuta:

```bash
mysql -u root -p < flask_app/SQL/schema.sql
```

Si tu servidor usa otro usuario, contraseña, host o puerto, modifica `.env`.

### 4. Configuración `.env`

```env
SECRET_KEY=bookhub-dev-secret-change-me
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DB=bookhub
```

Para GitHub, `.env` está excluido mediante `.gitignore`; usa `.env.example` como plantilla.

### 5. Ejecutar

```bash
python server.py
```

Abrir `http://localhost:5000`.

## Estructura MVC

```text
flask_app/
├── config/
│   └── mysqlconnection.py
├── controllers/
│   └── router.py
├── models/
│   ├── libros.py
│   └── usuarios.py
├── templates/
├── static/css/
└── SQL/
resources/
└── ERD.svg
server.py
requirements.txt
.env
.env.example
```

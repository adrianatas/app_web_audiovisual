### El objetivo del proyecto es desarrollar una aplicación web tipo plataforma de streaming audiovisual (películas y series) con una página principal, con una página de registro de usuario, inicio de sesión, cuenta de administrador, catalogo con las películas y series, con un apartado de búsqueda de la películas o series poniendo el nombre tanto el minúsculas como en mayúsculas, opción de que el usuario guarde elementos en visto y favoritos, pagina de cerrar sesión.

El stack tecnológico usado:

- Python 3.13
- Framework principal Flask porque me resulto más fácil

- SQLAlchemy para gestión de base de datos.
- Flask-Login para autentificación.
- Bootstrap para el diseño, HTML y CSS (el HTML y CSS los he puesto unidos, es decir en cada template/home.html, template/catalogo.html, template/login.html, etc es donde esta el CSS.)

- Explicación y esquema de la base de datos

Se implementaron tres tablas principales:
- User: usuarios con roles de admin/cliente
- Content: películas y series
- UserContent: relación entre usuarios y contenido (favorito/visto). Relación (un usuario puede tener muchos contenidos asociados)

Los requisitos de la aplicación:
Como lo he mencionado más arriba, la aplicación permite:
- registro y login
- roles diferentes
- visualización de catálogo
- marcar contenido como favorito o visto
- buscar contenido
- ver estadísticas personales

Instalación:
Instalar las librerías necesarias:

pip install flask flask_sqlalchemy flask_login

Ejecutar el archivo principal:

python main.py
 
Al ejecutar el proyecto por primera vez se crea la base de datos automáticamente (database.db); se crea el administrador: usuario: admin;
contraseña: admin123; se cargan contenidos de prueba (películas y series)

Acceder a la aplicación:

http://127.0.0.1:5000

Uso básico:
Registrarse como usuario nuevo o iniciar sesión. Acceder al catálogo. Marcar contenido como: 
                        favorito
                        visto
                        utilizar el buscador
                        acceder como admin para funciones administrativas 

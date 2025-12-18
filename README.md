# 🛒 Sistema E-Commerce Drawings Store

Aplicación web de comercio electrónico desarrollada como proyecto final. El sistema implementa una arquitectura **Full Stack** utilizando **Python (Flask)** para el backend y **HTML/CSS/JS** para el frontend, integrando una base de datos relacional **SQLite** gestionada mediante ORM.

La aplicación cuenta con un panel de administración robusto que cumple con todas las operaciones **CRUD** (Crear, Leer, Actualizar, Eliminar).

## 🛠️ Tecnologías Utilizadas

### Backend (Servidor y Lógica)
* **Python 3.x**: Lenguaje principal.
* **Flask**: Micro-framework para el manejo de rutas y servidor web.
* **SQLAlchemy**: ORM (Object-Relational Mapping) para la gestión y modelado de la base de datos.
* **Flask-Login**: Gestión de sesiones de usuario, protección de rutas y autenticación.
* **Werkzeug Security**: Encriptación de contraseñas (Hashing) para seguridad de datos.

### Frontend (Interfaz de Usuario)
* **HTML5 / Jinja2**: Estructura semántica y motor de plantillas dinámicas.
* **CSS3**: Hojas de estilo personalizadas (Diseño Responsivo).
* **JavaScript**: Validaciones básicas e interactividad del lado del cliente.

---

## ✨ Funcionalidades Principales

### 1. Módulo de Usuario (Cliente)
* **Autenticación:** Registro de nuevos usuarios y Login seguro.
* **Catálogo:** Visualización de productos disponibles.
* **Simulación de Compra:** Formulario de "Tramitar Pago" que registra órdenes en la base de datos vinculadas al usuario actual.

### 2. Módulo de Administrador (Panel de Control)
Acceso protegido exclusivamente para usuarios con rol `admin`. Incluye funcionalidades **CRUD Completo**:

* **Create (Crear):** Generación de usuarios y registros de órdenes (desde el flujo de compra).
* **Read (Leer):** Visualización tabular de todos los usuarios registrados y el historial completo de pedidos.
* **Update (Actualizar):**
    * Edición de nombres de usuario.
    * **Gestión de Roles:** Capacidad de promover usuarios a administradores o revocarlos.
* **Delete (Eliminar):**
    * Eliminación de órdenes de compra.
    * Eliminación de usuarios (con borrado en cascada de sus pedidos para mantener la integridad de la BD).

---

## 📂 Estructura del Proyecto

```text
PROYECTO-FINAL/
│
├── static/                  # Archivos estáticos (CSS, Imágenes, JS)
│   └── css/
│       └── admin.css        # Estilos específicos del panel
│
├── templates/               # Plantillas HTML (Jinja2)
│   ├── Inicio.html
│   ├── Login.html
│   ├── Admin.html           # Vista principal del Dashboard
│   ├── EditarUsuario.html   # Formulario de edición
│   └── ... (otras vistas)
│
├── app.py                   # Lógica principal del servidor y rutas
├── crear_admin.py           # Script para crear el primer superusuario
├── database.db              # Base de datos SQLite (se genera automáticamente)
└── README.md                # Documentación del proyecto
```
🚀 Instalación y Ejecución
Sigue estos pasos para ejecutar el proyecto en tu entorno local:

1. Prerrequisitos
Tener instalado Python y pip.

2. Instalación de Dependencias
Abre tu terminal en la carpeta del proyecto e instala las librerías necesarias:
pip install flask flask-sqlalchemy flask-login

3. Configuración Inicial (Primer uso)
Para crear la base de datos y el usuario administrador por defecto, ejecuta el script auxiliar:
python crear_admin.py
Esto generará el archivo database.db y creará al usuario admin.

4. Ejecutar el Servidor
Inicia la aplicación con el siguiente comando:
python app.py

5. Acceso
Abre tu navegador web e ingresa a: 👉 https://www.google.com/search?q=http://127.0.0.1:5000

🔑 Credenciales de Acceso (Admin)
Para acceder al Panel de Administración y probar las funciones CRUD:
Usuario: admin
Contraseña: 1234

from app import app, db, User
from werkzeug.security import generate_password_hash

# Esto permite interactuar con tu aplicación Flask
with app.app_context():
    # 1. Crear las tablas si no existen (por seguridad)
    db.create_all()

    # 2. Verificar si ya existe el admin para no duplicarlo
    usuario_existente = User.query.filter_by(username='admin').first()

    if not usuario_existente:
        # 3. Crear el usuario
        # Puedes cambiar '1234' por la contraseña que prefieras
        password_encriptada = generate_password_hash('1234', method='pbkdf2:sha256')

        nuevo_admin = User(
            username='admin', 
            password=password_encriptada, 
            role='admin'
        )
        
        # 4. Guardar en la base de datos
        db.session.add(nuevo_admin)
        db.session.commit()
        print("¡Usuario 'admin' creado con éxito! Contraseña: 1234")
    else:
        print("El usuario 'admin' ya existe en la base de datos.")
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#Configuracion del login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#Modelo de base de datos
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), default='user') # 'user' o 'admin'

#Crear la base de datos
with app.app_context():
    db.create_all()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def inicio():
    return render_template('Inicio.html')

@app.route('/productos')
def productos():
    return render_template('Productos.html')

@app.route('/nosotros')
def nosotros():
    return render_template('Nosotros.html')

@app.route('/contacto')
def contacto():
    return render_template('Contacto.html')

# --- RUTAS DE FUNCIONALIDAD (Backend) ---

# 1. Login y Registro (En la misma ruta para simplificar)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form.get('action') # Saber si es login o registro
        username = request.form.get('username')
        password = request.form.get('password')

        if action == 'register':
            # Lógica de Registro
            if User.query.filter_by(username=username).first():
                flash('El usuario ya existe', 'error')
            else:
                new_user = User(username=username, 
                                password=generate_password_hash(password, method='pbkdf2:sha256'),
                                role='user') # Por defecto usuario normal
                db.session.add(new_user)
                db.session.commit()
                flash('Cuenta creada. Ahora inicia sesión.', 'success')

        elif action == 'login':
            # Lógica de Login
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('inicio'))
            else:
                flash('Usuario o contraseña incorrectos', 'error')

    return render_template('Login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('inicio'))

# 2. Acción protegida: Tramitar Pago (Solo usuarios logueados)
@app.route('/tramitar-pago', methods=['GET', 'POST'])
@login_required
def tramitar_pago():
    if request.method == 'POST':
        # Aquí recibirías los datos del formulario final
        nombre = request.form.get('nombre')
        # Simulación de backend procesando compra
        flash(f'¡Gracias {nombre}! Tu pedido ha sido procesado por el servidor.', 'success')
        return redirect(url_for('inicio'))
        
    return render_template('TramitarPago.html', nombre_usuario=current_user.username)

# 3. Panel de Administración (Control de Roles)
@app.route('/admin')
@login_required
def admin_panel():
    if current_user.role != 'admin':
        flash('No tienes permiso para ver esta página', 'error')
        return redirect(url_for('inicio'))
    
    users = User.query.all() # El admin puede ver todos los usuarios
    return render_template('Admin.html', users=users) # Necesitarías crear un Admin.html simple o mostrar texto

if __name__ == '__main__':
    app.run(debug=True)
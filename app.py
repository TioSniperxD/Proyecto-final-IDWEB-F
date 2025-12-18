from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import datetime
app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
db = SQLAlchemy(app)

#Configuracion del login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#Modelo de base de datos
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), default='user')
    # Relación: Un usuario puede tener muchas órdenes
    ordenes = db.relationship('Orden', backref='comprador', lazy=True)
class Orden(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_titular = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    tarjeta = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    monto = db.Column(db.String(50), nullable=False, default='S/ 0.00')
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
        # 1. Recibir los datos del formulario HTML
        nombre = request.form.get('nombre')
        direccion = request.form.get('direccion')
        tarjeta = request.form.get('tarjeta')
        monto = request.form.get('monto')
        
        # 2. Crear la nueva orden en la base de datos
        nueva_orden = Orden(
            nombre_titular=nombre,
            direccion=direccion,
            tarjeta=tarjeta,
            monto=monto,
            user_id=current_user.id  # Guardamos el ID del usuario actual
        )
        
        # 3. Guardar cambios
        db.session.add(nueva_orden)
        db.session.commit()
        
        # 4. Mensaje de éxito y redirección
        flash(f'¡Pedido registrado exitosamente! Orden #{nueva_orden.id}', 'success')
        print(f"✅ Nueva compra registrada: {nombre} - {direccion}") # Mensaje en consola para verificar
        return redirect(url_for('inicio'))
        
    return render_template('TramitarPago.html', nombre_usuario=current_user.username)
# 3. Panel de Administración (Control de Roles)
@app.route('/admin')
@login_required
def admin_panel():
    if current_user.role != 'admin':
        flash('No tienes permiso para ver esta página', 'error')
        return redirect(url_for('inicio'))
    
    users = User.query.all()
    ordenes = Orden.query.all()
    
    # 🔴 CORRECCIÓN 1: Agregamos ordenes=ordenes para que se vean en la tabla
    return render_template('Admin.html', users=users, ordenes=ordenes)

# --- RUTA PARA ELIMINAR (Cumple con la D de CRUD) ---
@app.route('/eliminar-orden/<int:id>')
@login_required
def eliminar_orden(id):
    if current_user.role != 'admin':
        flash('No tienes permiso para hacer esto.', 'error')
        return redirect(url_for('inicio'))
    
    orden_a_borrar = Orden.query.get_or_404(id)
    
    try:
        db.session.delete(orden_a_borrar)
        db.session.commit()
        flash('La orden ha sido eliminada correctamente.', 'success')
    except:
        flash('Hubo un error al intentar borrar la orden.', 'error')
        
    return redirect(url_for('admin_panel'))    

@app.route('/eliminar-usuario/<int:id>')
@login_required
def eliminar_usuario(id):
    # 1. Seguridad: Solo admin puede entrar aquí
    if current_user.role != 'admin':
        flash('No tienes permiso para hacer esto.', 'error')
        return redirect(url_for('inicio'))

    # 2. Seguridad: No puedes borrarte a ti mismo
    if id == current_user.id:
        flash('¡No puedes eliminar tu propia cuenta de administrador!', 'error')
        return redirect(url_for('admin_panel'))

    # 3. Buscar y borrar
    usuario_a_borrar = User.query.get_or_404(id)
    
    try:
        # (Opcional) Borrar sus órdenes primero para no dejar basura en la DB
        Orden.query.filter_by(user_id=id).delete()
        
        # Borrar el usuario
        db.session.delete(usuario_a_borrar)
        db.session.commit()
        flash(f'El usuario {usuario_a_borrar.username} ha sido eliminado.', 'success')
    except:
        flash('Hubo un error al intentar eliminar el usuario.', 'error')

    return redirect(url_for('admin_panel'))
# --- RUTA PARA EDITAR (Cumple con la U de CRUD) ---
@app.route('/editar-usuario/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    # 1. Seguridad: Solo el admin puede entrar
    if current_user.role != 'admin':
        flash('No tienes permiso.', 'error')
        return redirect(url_for('inicio'))
    
    # 2. Buscar al usuario que queremos editar
    usuario_a_editar = User.query.get_or_404(id)

    # 3. Si le dimos al botón "Guardar" (Método POST)
    if request.method == 'POST':
        usuario_a_editar.username = request.form['username']
        usuario_a_editar.role = request.form['role']
        
        try:
            db.session.commit()
            flash('Usuario actualizado correctamente.', 'success')
            return redirect(url_for('admin_panel'))
        except:
            flash('Error al actualizar. Quizás el nombre ya existe.', 'error')

    # 4. Si solo estamos entrando a la página (Método GET)
    return render_template('EditarUsuario.html', user=usuario_a_editar)
if __name__ == '__main__':
    app.run(debug=True)
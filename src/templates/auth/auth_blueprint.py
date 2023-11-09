from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

csrf = CSRFProtect()
mysql= MySQL(app)
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(mysql, id)


# Login
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #print(request.form['username'])
        #print(request.form['password'])
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(mysql, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Invalid password...")
                return render_template('auth/login.html')
        else:
            flash("User not found...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/protected')
#Decorador para proteger las rutas
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404
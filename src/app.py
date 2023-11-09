# Librerías
import pandas as pd
import openpyxl
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
#Obtener dataframe csv
from io import StringIO

from config import config

from models.ModelUser import ModelUser
from models.entities.User import User



app = Flask(__name__)

# Login
csrf = CSRFProtect()
mysql= MySQL(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(mysql, id)


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
                flash("Usuario/Contraseña inválidos")
                return render_template('auth/login.html')
        else:
            flash("Usuario/Contraseña inválidos")
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
    
    




# Sistemas
@app.route('/sistemas')
@login_required
def sistemas():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM inventario")
    inventario_items = cur.fetchall()
    print(inventario_items)

    return render_template('sistemas/index.html', inv = inventario_items)

# Ruta para añadir elementos
@app.route('/add_insumo', methods=['POST'])  
def add_insumo():  
    if request.method == 'POST':
        insumos = request.form['insumos']
        registro = request.form['registro']
        ubicacion = request.form['ubicacion']
        estado = request.form['estado']
        precio_unitario = request.form['precio_unitario']
        fecha_de_ingreso = request.form['fecha_de_ingreso']
        fecha_de_actualizacion = request.form['fecha_de_actualizacion']
        observacion = request.form['observacion']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM inventario WHERE registro = %s", (registro,))
        existing_record = cur.fetchone()

        if existing_record:
            flash('No puedes añadir este elemento. Ya existe un registro con este valor.')
        else:
            cur.execute('INSERT INTO inventario (insumos, registro, ubicacion, estado, precio_unitario, fecha_de_ingreso, fecha_de_actualizacion, observacion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (insumos, registro, ubicacion, estado, precio_unitario, fecha_de_ingreso, fecha_de_actualizacion, observacion))
            mysql.connection.commit()
            flash('Insumo ingresado correctamente')

        return redirect('/sistemas')

# Ruta para recuperar la información disponible en la DB para poder editar un elemento
@app.route('/edit_insumo/<int:id>')
def edit_insumo(id):

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM inventario WHERE id = %s', (id,))
    inventario_items = cur.fetchall()
    mysql.connection.commit() 
    
    return render_template('/sistemas/editsistemas.html', inv = inventario_items) 

# Ruta para editar elementos dela base de datos
@app.route('/update/<id>', methods = ['POST']) 
def update(id):
    if request.method == 'POST':
        insumos = request.form['insumos']
        registro = request.form['registro']
        ubicacion = request.form['ubicacion']
        estado = request.form['estado']
        precio_unitario = request.form['precio_unitario']
        fecha_de_ingreso = request.form['fecha_de_ingreso']
        fecha_de_actualizacion = request.form['fecha_de_actualizacion']
        observacion = request.form['observacion']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM inventario WHERE registro = %s AND id != %s", (registro, id))
        existing_record = cur.fetchone()

        if existing_record:
            flash('No puedes editar este elemento. Ya existe un registro con este valor.')
        else:
            cur.execute("""
                        UPDATE inventario
                        SET insumos = %s, registro = %s, ubicacion  = %s, estado = %s, 
                            precio_unitario = %s, fecha_de_ingreso = %s, fecha_de_actualizacion = %s,
                            observacion = %s WHERE id = %s
                        """, (insumos, registro, ubicacion, estado, precio_unitario, fecha_de_ingreso,
                            fecha_de_actualizacion, observacion, id))
            mysql.connection.commit()
            flash(f'Elemento con id {id} editado correctamente')

        return redirect('/sistemas')

# Ruta para eliminar elementos
@app.route('/delete_insumo/<int:id>')
def delete_insumo(id):
      
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM inventario WHERE id = %s', (id,))  
    mysql.connection.commit()       
    (flash(f'Elemento con id #{id} eliminado correctamente')) 
    return redirect('/sistemas')


# Descarga Excel
@app.route('/obtener_excel', methods=['GET'])
def obtener_excel():

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM inventario')
    data = cur.fetchall()
    cur.close()
    
    df = pd.DataFrame(data, columns = ["id", "insumos", "registro", "ubicacion", "estado", "precio_unitario", "fecha_de_ingreso", "fecha_de_actualizacion", "observacion"])
    
    excel_filename = "inventario.xlsx"
    df.to_excel(excel_filename, index=False)

    return send_file(f'../{excel_filename}', as_attachment=True)

# Función Excel
@app.route('/descargar')
def descargar():
    return obtener_excel()


#Descarga CSV
@app.route('/obtener_csv', methods=['GET'])
def obtener_csv():

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM inventario')
    data = cur.fetchall()
    cur.close()
    
    df = pd.DataFrame(data, columns = ["id", "insumos", "registro", "ubicacion", "estado", "precio_unitario", "fecha_de_ingreso", "fecha_de_actualizacion", "observacion"])

    csv_output = StringIO()
    df.to_csv(csv_output, index=False)
    
    csv_filename = "inventario.csv"
    with open(csv_filename, 'w') as csv_file:
        csv_file.write(csv_output.getvalue())
    csv_output.close()
    print(f"Archivo CSV guardado en la ubicación: {csv_filename}")

    return send_file(f'../{csv_filename}', as_attachment=True)

#Función CSV
@app.route('/descargar_csv')
def descargar_csv():
    return obtener_csv()


if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(debug=True, port=8000)



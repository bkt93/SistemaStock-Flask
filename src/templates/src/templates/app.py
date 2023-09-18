from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)


# Conexión a la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'invmysql'
app.config['MYSQL_DB'] = 'inventarioflask'

mysql= MySQL(app)



# Ruta principal
@app.route('/')
def Index():


    # Consulta SELECT para acceder a todos los datos de la db
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM inventario")
    inventario_items = cur.fetchall()
    print(inventario_items)

    return render_template('index.html', inv = inventario_items)

    
# Ruta para renderizar el template para añadir nuevos elementos
@app.route("/create")
def create():
    return render_template("create.html")

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
        cur.execute('INSERT INTO inventario (insumos, registro, ubicacion, estado, precio_unitario, fecha_de_ingreso, fecha_de_actualizacion, observacion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (insumos, registro, ubicacion, estado, precio_unitario, fecha_de_ingreso, fecha_de_actualizacion, observacion))
        mysql.connection.commit()
        return redirect('/')

# Ruta para recuperar la información disponible en la DB para poder editar un elemento
@app.route('/edit_insumo/<int:id>')
def edit_insumo(id):

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM inventario WHERE id = %s', (id,))
    inventario_items = cur.fetchall()
    mysql.connection.commit()
    return render_template('edit.html', inv = inventario_items)


# Consulta UPDATE para actualizar elementos de la DB
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
        cur.execute("""
                    UPDATE inventario
                    SET insumos = %s, registro = %s, ubicacion  = %s, estado = %s, 
                        precio_unitario = %s, fecha_de_ingreso = %s, fecha_de_actualizacion = %s,
                        observacion = %s WHERE id = %s
                    """, (insumos, registro, ubicacion, estado, precio_unitario, fecha_de_ingreso,
                        fecha_de_actualizacion, observacion, id))
        mysql.connection.commit()
        return redirect('/')

# Ruta para eliminar elementos
@app.route('/delete_insumo/<int:id>')
def delete_insumo(id):
      
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM inventario WHERE id = %s', (id,))
    mysql.connection.commit()        
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=8000)


from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Conexión a la base de datos MySQL



@app.route('/')
def Index():
    return render_template('index.html')

# Ruta para añadir elementos
@app.route('/add_insumo', methods=['POST'])
def add_insumo():
    if request.method == 'POST':
        insumo = request.form['insumo']
        registro = request.form['registro']
        ubicacion = request.form['ubicacion']
        estado = request.form['estado']
        precio_unitario = request.form['precio_unitario']
        fecha_de_ingreso = request.form['fecha_de_ingreso']
        fecha_de_actualización = request.form['fecha_de_actualizacion']
        observacion = request.form['observacion']
        
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO inventario (insumo, registro, ubicacion, estado, precio_unitario, fecha_de_ingreso, fecha_de_actualizacion, observacion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (insumo, registro, ubicacion, estado, precio_unitario, fecha_de_ingreso, fecha_de_actualización, observacion))
        mysql.connection.commit()
        return "Recibido"

# Ruta para editar elementos
@app.route('/edit_insumo')
def edit_insumo():
    return "Elemento editado"

# Ruta para eliminar elementos
@app.route('/delete_insumo')
def delete_insumo():
    return "Elemento eliminado"

if __name__ == '__main__':
    app.run(debug=True)



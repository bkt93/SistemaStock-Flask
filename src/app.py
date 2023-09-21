from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


from config import config

app = Flask(__name__)

mysql= MySQL(app)


# Ruta principal
@app.route('/')
def Index():

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
        cur.execute('INSERT INTO inventario (insumos, registro, ubicacion, estado, precio_unitario, fecha_de_ingreso, fecha_de_actualizacion, observacion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (insumos, registro, ubicacion, estado, precio_unitario, fecha_de_ingreso, fecha_de_actualizacion, observacion))
        mysql.connection.commit()
        flash('Insumo ingresado')
        return redirect('/')

# Ruta para recuperar la información disponible en la DB para poder editar un elemento
@app.route('/edit_insumo/<int:id>')
def edit_insumo(id):

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM inventario WHERE id = %s', (id,))
    inventario_items = cur.fetchall()
    mysql.connection.commit()
    
   
    return render_template('edit.html', inv = inventario_items)

# Ruta para editar elementos
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
        flash('Hecho!')
        return redirect('/')

# Ruta para eliminar elementos
@app.route('/delete_insumo/<int:id>')
def delete_insumo(id):
      
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM inventario WHERE id = %s', (id,))
    mysql.connection.commit()       
    flash('Elemento eliminado!') 
    return redirect('/')


#RUTAS SECTOR FINANZAS


#Ruta finanzas
@app.route("/finanzas")
def finanzas():
    
    # Consulta SELECT para acceder a todos los datos de la db
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM finanzas")
    finanzas_items = cur.fetchall()
    print(finanzas_items)

    return render_template('finanzas.html', fin = finanzas_items)


# Ruta para renderizar el template para añadir nuevos elementos
@app.route("/create_fin")
def create_fin():
    return render_template("create_fin.html")

# Ruta para añadir elementos
@app.route('/add_insumo_fin', methods=['POST'])
def add_insumo_fin():
    if request.method == 'POST':
        numero_de_registro = request.form['numero_de_registro']
        clasificacion = request.form['clasificacion']
        detalle_del_bien = request.form['detalle_del_bien']
        edificio = request.form['edificio']
        area_responsable = request.form['area_responsable']
        estado = request.form['estado']
        valor_unitario = request.form['valor_unitario']
                
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO finanzas (numero_de_registro, clasificacion, detalle_del_bien, edificio, area_responsable, estado, valor_unitario) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                    (numero_de_registro, clasificacion, detalle_del_bien, edificio, area_responsable, estado, valor_unitario))
        mysql.connection.commit()
        flash('Registro ingresado')
        return redirect('/finanzas')




# # Ruta de busqueda de elementos
# @app.route('/buscar', methods=['GET', 'POST'])
# def index():
#     results = []

#     if request.method == 'POST':
#         query = request.form['query']
#         # Llama a tu función para buscar en la base de datos
#         results = buscar_en_bd(query)
        
#         if not results:
#             results = ["Vacío: El valor no existe en la base de datos."]

#     return render_template('index.html', results=results)






 

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(debug=True, port=8000)



import pandas as pd
import openpyxl
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_mysqldb import MySQL



from config import config

app = Flask(__name__)

mysql= MySQL(app)


# Login
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form['username'])
        print(request.form['password'])
        return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


# Ruta principal
@app.route('/sistemas')
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


#RUTAS DE IP-BOX

# Ruta ppal ip-box
@app.route('/ip_box')
def ip_box():
    # Consulta para acceder a los datos de la DB ip_box
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM ip_box")
    ip_box_items = cur.fetchall()
    print(ip_box_items)

    return render_template('ipbox/ip_box.html', ip_box = ip_box_items)

# Ruta para añadir elementos

@app.route("/create_ip")
def create_ip():
    return render_template("ipbox/create_ip.html")


@app.route('/add_ip', methods=['POST'])
def add_ip():
    if request.method == 'POST':
        ip = request.form['ip']
        inventario = request.form['inventario']
        hostname = request.form['hostname']
        extension = request.form['extension']
        contrasena = request.form['contrasena']
        box = request.form['box']
        sector = request.form['sector']
        fecha_de_actualizacion = request.form['fecha_de_actualizacion']
        observacion = request.form['observacion']
    
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO ip_box (ip, inventario, hostname, extension, contrasena, box, sector, fecha_de_actualizacion, observacion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (ip, inventario, hostname, extension, contrasena, box, sector, fecha_de_actualizacion, observacion))
        mysql.connection.commit()
        flash('IP ingresado')
        return redirect('ipbox/ip_box.html')
    
  
# Ruta para editar elementos
@app.route('/editar_ip/<int:ip>', methods = ['POST'])
def editar_ip(ip):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM ip_box WHERE id = %s', (ip,))
    ip_box_items = cur.fetchall()
    mysql.connection.commit()    
   
    return render_template('ipbox/edit_ip.html', inv_ip = ip_box_items)

# Ruta para editar elementos
@app.route('/update_ip/<ip>', methods = ['POST'])
def update_ip(ip):
    if request.method == 'POST':
        ip = request.form['ip']
        inventario = request.form['inventario']
        hostname = request.form['hostname']
        extension = request.form['extension']
        contrasena = request.form['contrasena']
        box = request.form['box']
        sector = request.form['sector']
        fecha_de_actualizacion = request.form['fecha_de_actualizacion']
        observacion = request.form['observacion']
        
        cur = mysql.connection.cursor()
        cur.execute("""
                    UPDATE ip_box
                    SET ip = %s, inventario = %s, hostname  = %s, extension = %s, 
                        contraseña = %s, box = %s, sector = %s,
                        fecha_de_actualizacion = %s, observacion = %s WHERE id = %s
                    """, (ip, inventario, hostname, extension, contrasena, box,
                        sector, fecha_de_actualizacion, observacion))
        mysql.connection.commit()
        flash('Hecho!')
        return redirect('ipbox/ip_box.html')






#RUTAS SECTOR FINANZAS


# #Ruta finanzas
# @app.route("/finanzas")
# def finanzas():
    
#     # Consulta SELECT para acceder a todos los datos de la db
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM finanzas")
#     finanzas_items = cur.fetchall()
#     print(finanzas_items)

#     return render_template('finanzas.html', fin = finanzas_items)


# # Ruta para renderizar el template para añadir nuevos elementos
# @app.route("/create_fin")
# def create_fin():
#     return render_template("create_fin.html")


# # Ruta para añadir elementos
# @app.route('/add_insumo_fin', methods=['POST'])
# def add_insumo_fin():
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


#crea una funcion para descargar la base de datos a Excel
@app.route('/obtener_excel', methods=['GET'])
def obtener_excel():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM inventario')
    data = cur.fetchall()
    cur.close()
    
    #Crear DataFrame
    df = pd.DataFrame(data, columns = ["id", "insumos", "registro", "ubicacion", "estado", "precio_unitario", "fecha_de_ingreso", "fecha_de_actualizacion", "observacion"])
    
    #Se guarda el data_frame en un Excel
    excel_filename = "inventario.xlsx"
    df.to_excel(excel_filename, index=False)

    #return 'Archivo descargado'
    return send_file(f'../{excel_filename}', as_attachment=True)


@app.route('/descargar')
def descargar():
    return obtener_excel()

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(debug=True, port=8000)



from flask import Flask, render_template, request, redirect, url_for
import os 
import database as db

#acceder a las los templates index.html---vistas
template_dir= os.path.dirname(os.path.abspath(os.path.dirname(__file__))) #indicar el nombre del directorio donde estara la aplicacion
template_dir = os.path.join(template_dir, "src","templates")# unimos el path del template... la idea es que siempre encuentre la ruta


app = Flask(__name__, template_folder=template_dir) #inicializamos flask , junto con el template folder que contiene el path a los archivos

#RUTA DEL HOME
@app.route('/')
def home():
    #crear cursor para acceder a la base de datos
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM contacts") #con esto tendremos acceso a todos los datos de la tabla de la base de datos----
    #crear objeto sql-dupla
    myresult= cursor.fetchall()#para hacer la consulta y/o llamado a la db
    #convertir los datos a diccionario  para acceder de manera correcta
    #creamos un arreglo vacio 
    insertObject=[]

    columNames = [column[0] for column in cursor.description] #con esto accedemos a la descripcion de los nombres de columna
    for record in myresult:
        insertObject.append(dict(zip(columNames, record))) ##por cada nombre de columna(columName), guardar su dato(record)
    cursor.close()# cerramos el cursor en el bucle

    return(render_template('index.html', data=insertObject)) #se le pasa tambien insertObject para poder iterar en el y mostrar los datos


#RUTA PARA GUARDAR---CREAR USUARIOS EN LA BASE DE DATOS----CREATE
@app.route('/user', methods=["POST"]) #nos vamos al index.html y en la etiqueta form y en href='/user'--- colocamos la ruta
def addUser():
    username= request.form['username']#el username viene del index.html.. va campo por campo---- name=username
    name= request.form['name']#el username viene del index.html.. va campo por campo---- name=name
    password= request.form['password']#el username viene del index.html.. va campo por campo---- name=password
    
    if username and name and password:
        cursor = db.database.cursor()
        sql= "INSERT INTO contacts (username, name, password) VALUES (%s, %s, %s)"
        data=(username,name,password)
        cursor.execute(sql, data)
        db.database.commit()#con esto se materializa la consulta 

    return redirect(url_for('home'))

#RUTA PARA ELIMINAR ---DELETE 
@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql= "DELETE FROM contacts WHERE id=%s"
    data=(id,)
    cursor.execute(sql, data)
    db.database.commit()#con esto se materializa la consulta 
    return redirect(url_for('home'))

#RUTA PARA ACTUALIZAR ----UPDATE---------------
@app.route('/edit/<string:id>' ,  methods=["POST"])
def edit(id):
    username= request.form['username']
    name= request.form['name']
    password= request.form['password']

    if username and name and password:
        cursor = db.database.cursor()
        sql= "UPDATE  contacts SET username=%s, name=%s, password=%s WHERE id=%s"
        data=(username,name,password, id)### OJO AQUI SE AGREGA EL ID-----
        cursor.execute(sql, data)
        db.database.commit()#con esto se materializa la consulta 

    return redirect(url_for('home'))


## IMPORTANTE ESTO SIEMPRE VA AL FINAL

if __name__ == '__main__':
    app.run(debug=True)



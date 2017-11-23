# -*- coding: utf-8 -*-

from flask import Flask, render_template, session
from flask import request, redirect, url_for
import shelve
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')


app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/')
def index():
    username = None

    if 'username' in session:
        username = session['username']
        db = shelve.open('datos.dat')
        datos = db[username]
        db.close()
        return render_template('indexLogin.html', usuario = username, profile = datos)
    
    return render_template('index.html', usuario = username)



@app.route('/login', methods=['GET','POST'])
def login():
	username = None
	if (request.method == 'POST'):
		
		db = shelve.open('datos.dat')
		#Compruebo que existe el usuario, en caso de no existir devolverá false
		flag = request.form['username'] in  db
		
		if flag:
			datos = db[request.form['username']]
			if (datos['Contrasenia'] == request.form['password']):
				session['username'] = request.form['username']		
		db.close()
		return redirect(url_for('index'))

	return render_template('login.html')


@app.route('/logout', methods=['GET','POST'])
def logout():
	session.pop('username', None)
	return redirect(url_for('index'))


@app.route('/register', methods=['GET','POST'])
def register():
                     
    if (request.method == 'POST'):
    	db = shelve.open('datos.dat')
    	db[request.form['username']] = {'Nombre': request.form['first_name'],
        								'Apellidos': request.form['last_name'],
        								'Correo': request.form['email'],
        								'Telefono': request.form['telephone'],
        								'Nombre de usuario': request.form['username'],
        								'Contrasenia': request.form['password']}
    	db.close()
    	return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/profile', methods=['GET','POST'])
def profile():
    username = session['username']
    db = shelve.open('datos.dat')
    datos = db[username]
    db.close()
    
    return render_template('indexLogin.html', profile = datos, usuario= username)


@app.route('/saveProfile', methods=['GET','POST'])
def save():
    username = session['username']
    db = shelve.open('datos.dat')
    db[username] = {'Nombre': request.form['first_name'],
                    'Apellidos': request.form['last_name'],
                    'Correo': request.form['email'],
                    'Telefono': request.form['telephone'],
                    'Nombre de usuario': username,
                    'Contrasenia': request.form['password']}
    db.close()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET','POST'])
def search():

	# Obtener base de datos
	db = client['test']

	# Obtener nuestra colección de la base de datos
	restaurants = db.restaurants


	query = request.form['tipoBusqueda']

	print(query)

	keyword = request.form['keyword']


	#Buscamos ahora lo que nos interesa
	respuesta = []


	# Cuando lo que queremos consultar está dentro de un "array"
	if(query == "zipcode" or query == "street"):
		query = "address." + query


	#La búsqueda nos devuelve un puntero iterable, así que extraemos el contenido	
	for r in restaurants.find({query : keyword}):
	   respuesta.append(r)
	

	return render_template('search.html', respuesta= respuesta)


def page_not_found(error):
    return render_template('error.html', err = error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # 0.0.0.0 para permitir conexiones
                                         #         desde cualquier sitio.
                                         #         Ojo, peligroso: solo
                                         #         en modo debug





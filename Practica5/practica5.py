# -*- coding: utf-8 -*-

from flask import Flask, render_template, session
from flask import request, redirect, url_for, jsonify
import shelve
from lxml import etree
import xml.etree.cElementTree as ET

from pymongo import MongoClient

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
	usuario = None
	if'username' in session: 
		usuario = session['username']

	query = request.form['tipoBusqueda']
	keyword = request.form['keyword']
	busqueda = query
	# Cuando lo que queremos consultar está dentro de un "array"
	if(query == "zipcode" or query == "street"):
		query = "address." + query

	return render_template('search.html', tipoBusqueda = query, palabraClave = keyword, usuario = usuario)

def buscarRestaurantes(query, keyword, pagina, maxElem, numeroElementos):

	client = MongoClient('mongodb://localhost:27017/')
	# Obtener base de datos
	db = client['test']
	# Obtener nuestra colección de la base de datos
	restaurants = db.restaurants
	busqueda = []
    #La búsqueda nos devuelve un puntero iterable, así que extraemos el contenido
	
	rang_min = int(numeroElementos)
	rang_max = int(numeroElementos) + int(maxElem)
	
	for r in restaurants.find({query : keyword}).sort("name")[rang_min:rang_max]:
		diccionario = { "name": r['name'], 
					"cuisine": r['cuisine'], 
					"street": r['address']['street'], 
					"building" : r['address']['building'], 
					"zipcode" : r['address']['zipcode'], 
					"borough" : r['borough'] }
		busqueda.append(diccionario)

	return busqueda


@app.route('/busqueda_restaurantes')
def responde():
	pagina = request.args.get('pagina', '')
	maxElementos = request.args.get('maxElem', '')
	query = request.args.get('query', '')
	keyword = request.args.get('keyword', '')
	numeroElementos = request.args.get('numElementos', '')
	

	busqueda = buscarRestaurantes(query, keyword, pagina, maxElementos, numeroElementos)
	return jsonify({'busqueda' :busqueda})





def page_not_found(error):
    return render_template('error.html', err = error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # 0.0.0.0 para permitir conexiones
                                         #         desde cualquier sitio.
                                         #         Ojo, peligroso: solo
                                         #         en modo debug





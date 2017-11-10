# -*- coding: utf-8 -*-

from flask import Flask, render_template, session
from flask import request, redirect, url_for
import shelve

historial = 0
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'



@app.route('/')
def index():

    username = None
    global historial
    if(historial >= 0):
        history = session
    else:
        history = None
    if 'username' in session:
        username = session['username']
        db = shelve.open('datos.dat')
        datos = db[username]
        db.close()
        return render_template('indexLogin.html', usuario = username, profile = datos, historial = history)
    return render_template('index.html', usuario = username, historial = history)


@app.route('/login', methods=['GET','POST'])
def login():
    username = None
    if (request.method == 'POST'):
        db = shelve.open('datos.dat')
        #Compruebo que existe el usuario, en caso de no existir devolverá false
        flag = request.form['username'] in  db
        if flag:
            datos = db[request.form['username']]
            db.close()
            if (datos['Contrasenia'] == request.form['pass']):
                session['username'] = request.form['username']
    return redirect(url_for('index'))


@app.route('/logout', methods=['GET','POST'])
def logout():
    if request.method == 'POST':
        session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    db = shelve.open('datos.dat')
                         
    if (request.method == 'POST'):
        db[request.form['username']] = {'Nombre': request.form['nombre'],
                                        'Apellidos': request.form['apellidos'],
                                        'DNI': request.form['dni'],
                                        'Correo': request.form['correo'],
                                        'Telefono': request.form['telefono'],
                                        'Nombre de usuario': request.form['username'],
                                        'Contrasenia': request.form['pass']}
    db.close()
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET','POST'])
def profile():
    username = session['username']
    db = shelve.open('datos.dat')
    datos = db[username]
    db.close()
    
    return render_template('indexLogin.html', profile = datos, usuario= username)

@app.route('/modify', methods=['GET','POST'])
def modify():
    username = session['username']
    db = shelve.open('datos.dat')
    datos = db[username]
    db.close()
    return render_template('indexLogin.html', usuario= username, profile = datos)

@app.route('/saveProfile', methods=['GET','POST'])
def save():
    username = session['username']
    db = shelve.open('datos.dat')
    db[username] = {'Nombre': request.form['nombre'],
                    'Apellidos': request.form['apellidos'],
                    'DNI': request.form['dni'],
                    'Correo': request.form['correo'],
                    'Telefono': request.form['telefono'],
                    'Nombre de usuario': username,
                    'Contrasenia': request.form['pass']}
    db.close()
    return redirect(url_for('index'))

@app.before_request
def before_request():
    
    url = request.url

    global historial
    if("http://127.0.0.1:8080/static/iconos/iconohtml.png" == url):
        return None
    if("http://127.0.0.1:8080/favicon.ico" == url):
        return None
    if("http://127.0.0.1:8080/static/style.css" == url):
        return None
    if("http://127.0.0.1:8080/static/images/HTML5.png" == url):
        return None

        
    if(historial == 0):
        session['page1'] = url
        print("primerapagina",session['page1'])
        historial = historial + 1
    elif(historial == 1):
        session['page2'] = url
        print("segundapagina", session['page2'])
        historial = historial + 1
    elif(historial == 2):
        session['page3'] = url
        print("tercerapagina", session['page3'])
        historial = 0

    
    

def page_not_found(error):
    return render_template('error.html', err = error)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # 0.0.0.0 para permitir conexiones
                                         #         desde cualquier sitio.
                                         #         Ojo, peligroso: solo
                                         #         en modo debug

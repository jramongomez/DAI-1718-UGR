# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask import request, redirect, url_for

app = Flask(__name__)

@app.route('/')                         # decorador, varia los parametros
def hello_world():                      # I/O de la función
    return render_template('home.html')

@app.route('/user/', methods=['GET','POST'])
@app.route('/user/<user>', methods=['GET','POST'])
def user(user=None):
	if request.method == 'POST':
		parametro1 = request.form['username']		
		return redirect(url_for('user', user=parametro1))
	return render_template('user.html', usuario = user)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', err = error)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # 0.0.0.0 para permitir conexiones
                                         #         desde cualquier sitio.
                                         #         Ojo, peligroso: solo
                                         #         en modo debug

	#if (parametro1 == None):
	#	parametro1 = user
    #else:
    #	parametro1 = user
#parametro1 = request.args.get('username')
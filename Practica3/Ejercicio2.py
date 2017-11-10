# -*- coding: utf-8 -*-

from flask import Flask, render_template, session
from flask import request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/')
def index():
    username = None
    if 'username' in session:
        username = session['username']
    return render_template('index.html', usuario = username)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
    return redirect(url_for('index'))


@app.route('/logout', methods=['GET','POST'])
def logout():
    if request.method == 'POST':
        session.pop('username', None)
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', err = error)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # 0.0.0.0 para permitir conexiones
                                         #         desde cualquier sitio.
                                         #         Ojo, peligroso: solo
                                         #         en modo debug

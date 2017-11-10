# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask import request, redirect, url_for


app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', err = error)

@app.route('/', methods=['GET','POST'])
def home():
    return render_template('home.html')



if __name__ == '__main__':
    
    app.run(host='0.0.0.0', debug=True)  # 0.0.0.0 para permitir conexiones
                                         #         desde cualquier sitio.
                                         #         Ojo, peligroso: solo
                                         #         en modo debug

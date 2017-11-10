# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask import request

app = Flask(__name__)

@app.route('/')                         # decorador, varia los parametros
def hello_world():                      # I/O de la función
    return render_template('welcome.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # 0.0.0.0 para permitir conexiones
                                         #         desde cualquier sitio.
                                         #         Ojo, peligroso: solo
                                         #         en modo debug
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask import request, redirect, url_for
from mandelbrot import *
from random import randint


app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', err = error)


@app.route('/', methods=['GET','POST'])
def index():
    random = randint(1, 4)
    x = randint(1,700)
    x2 = randint(1,700)
    y = randint(1,500)
    y2 = randint(1,500)
    rx = randint(1,700)
    ry = int(rx / 2)
    color = generarColorHTML()
    

    return render_template('svg.html', aleatorio = random, x= x, y = y, rx = rx, ry= ry, x2 = x2, y2 = y2, color = color)


def generarColorHTML():
    color = "#"
    string = ""
    number = 0
    for i in range(6):
        rand = randint(0,15)
        if(rand >9):
            string = hex(rand)
            string = string[2]
            color = color + string
        else:
            color = color + str(rand)
    return color

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', debug=True)  # 0.0.0.0 para permitir conexiones
                                         #         desde cualquier sitio.
                                         #         Ojo, peligroso: solo
                                         #         en modo debug

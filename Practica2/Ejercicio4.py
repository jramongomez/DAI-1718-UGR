# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask import request, redirect, url_for
from mandelbrot import *

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', err = error)


@app.route('/', methods=['GET','POST'])
def index():
    return render_template('fractalForm.html')



@app.route('/generaFractal', methods=['GET','POST'])
def generaFractal():
    x1 = float(request.args.get('x1'))
    x2 = float(request.args.get('x2'))
    y1 = float(request.args.get('y1'))
    y2 = float(request.args.get('y2'))
    anchura = int(request.args.get('anchura'))
    iteraciones = int(request.args.get('iteraciones'))

    color1 = (request.args.get('color1'))
    color2 = (request.args.get('color2'))
    color3 = (request.args.get('color3')) 
    if (not((color1 == "#000000") and (color2 == "#000000") and (color3 == "#000000"))): 
        #Cada color en HTML tiene el siguiente formato: rrggbb, por tanto separamos cada color en una lista de 3 tuplas (r,g,b). 
        color1 = color1[1:]
        color2 = color2[1:]
        color3 = color3[1:]
        paleta = ((int(color1[:2], 16), int(color1[2:4], 16), int(color1[4:], 16)),
        (int(color2[:2], 16), int(color2[2:4], 16), int(color2[4:], 16)),
        (int(color3[:2], 16), int(color3[2:4], 16), int(color3[4:], 16)))
        renderizaMandelbrotBonito(x1,y1,x2,y2,anchura, iteraciones, "fractal.png", paleta, len(paleta))
    else:
        renderizaMandelbrot(x1,y1,x2,y2,anchura, iteraciones, "fractal.png")

    return render_template('generaFractal.html')



if __name__ == '__main__':
    
    app.run(host='0.0.0.0', debug=True)  # 0.0.0.0 para permitir conexiones
                                         #         desde cualquier sitio.
                                         #         Ojo, peligroso: solo
                                         #         en modo debug

#!/usr/bin/env python
import logging

from flask import Flask, render_template, request
from flask_basicauth import BasicAuth

from cage import Cage

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'micha'
app.config['BASIC_AUTH_PASSWORD'] = 'lovesspiders'

# initial config
cages = [
    Cage(name='spider 1',
         sensor_chan=2,
         lamp_pin=29,
         pump_pin=32,
         temp_goal=30,
         temp_prec=2,
         hum_threshold=60),
    Cage(name='spider 2',
         sensor_chan=3,
         lamp_pin=31,
         pump_pin=36,
         temp_goal=27,
         temp_prec=2,
         hum_threshold=40)
]

basic_auth = BasicAuth(app)

@app.route('/', methods = ['GET', 'POST'])
@basic_auth.required
def home():
    if request.method == 'POST':
        try: 
            logging.info(request.form)
            if 'btn' in request.form and request.form['btn'] == 'refresh':
                for cage in cages:
                    cage.read_sensor()
            if 'lamp-on' in request.form:
                logging.info(request.form['lamp-on'])
                index = int(request.form['lamp-on'])-1
                cages[index].setLamp(True)
                cages[index].lamp_auto = False
            if 'lamp-off' in request.form:
                index = int(request.form['lamp-off'])-1
                cages[index].setLamp(False)
                cages[index].lamp_auto = False
            if 'lamp-auto' in request.form:
                index = int(request.form['lamp-auto'])-1
                cages[index].lamp_auto = True
            if 'pump-pulse' in request.form:
                index = int(request.form['pump-pulse'])-1
                cages[index].pulsePump()
        except Exception as e:
            logging.exception(e)
    
    return render_template('home.html', cages=cages)

if __name__ == '__main__':
    app.run(debug=True)

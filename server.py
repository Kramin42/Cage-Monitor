#!/usr/bin/env python
import logging

from flask import Flask, render_template
from flask_basicauth import BasicAuth

from cage import Cage

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'micha'
app.config['BASIC_AUTH_PASSWORD'] = 'lovesspiders'

# initial config
cages = [
    Cage(name='cage 1',
         sensor_chan=2,
         lamp_pin=29,
         pump_pin=32,
         temp_goal=30,
         temp_prec=2,
         hum_goal=80,
         hum_prec=20)
]

basic_auth = BasicAuth(app)

@app.route('/')
@basic_auth.required
def secret_view():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)

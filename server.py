#!/usr/bin/env python
import logging
import time
import atexit
import os
import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask, render_template, request
from flask_basicauth import BasicAuth

from cage import Cage

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

#-Configuration--(Edit Here)---------------------------------------------------
app.config['BASIC_AUTH_USERNAME'] = 'micha'
app.config['BASIC_AUTH_PASSWORD'] = 'lovesspiders'

global_time_start = datetime.time(9) # 9 am
global_time_stop = datetime.time(21) # 9 pm

# How often the tempurature/humidity are checked
# to automatically switch the lamps/pumps
update_interval = 60 #  seconds

cages = [
    Cage(name='spider 1',
         sensor_chan=2,
         lamp_pin=29,
         pump_pin=32,
         temp_goal=30,
         temp_prec=2,
         hum_threshold=60,
         time_start=global_time_start,
         time_stop=global_time_stop),
    Cage(name='spider 2',
         sensor_chan=3,
         lamp_pin=31,
         pump_pin=36,
         temp_goal=27,
         temp_prec=2,
         hum_threshold=40,
         time_start=global_time_start,
         time_stop=global_time_stop),
    Cage(name='spider 3',
         sensor_chan=4,
         lamp_pin=31,
         pump_pin=36,
         temp_goal=27,
         temp_prec=2,
         hum_threshold=40,
         time_start=global_time_start,
         time_stop=global_time_stop),
    Cage(name='spider 4',
         sensor_chan=14,
         lamp_pin=31,
         pump_pin=36,
         temp_goal=27,
         temp_prec=2,
         hum_threshold=40,
         time_start=global_time_start,
         time_stop=global_time_stop),
    Cage(name='spider 5',
         sensor_chan=15,
         lamp_pin=31,
         pump_pin=36,
         temp_goal=27,
         temp_prec=2,
         hum_threshold=40,
         time_start=global_time_start,
         time_stop=global_time_stop),
    Cage(name='spider 6',
         sensor_chan=17,
         lamp_pin=31,
         pump_pin=36,
         temp_goal=27,
         temp_prec=2,
         hum_threshold=40,
         time_start=global_time_start,
         time_stop=global_time_stop),
    Cage(name='spider 7',
         sensor_chan=18,
         lamp_pin=31,
         pump_pin=36,
         temp_goal=27,
         temp_prec=2,
         hum_threshold=40,
         time_start=global_time_start,
         time_stop=global_time_stop),
    Cage(name='spider 8',
         sensor_chan=27,
         lamp_pin=31,
         pump_pin=36,
         temp_goal=27,
         temp_prec=2,
         hum_threshold=40,
         time_start=global_time_start,
         time_stop=global_time_stop),
]
#------------------------------------------------------------------------------

# sensors are on GPIO channels  2,  3,  4, 14, 15, 17, 18, 27
# which are pins                3,  5,  7,  8, 10, 11, 12, 13
# need to use the channel number in sensor_chan=x

# lamps are on pins 15, 16, 18, 19, 21, 22
# pumps are on pins 35, 36, 37, 38, 40

def update_all():
    for cage in cages:
        cage.check_and_update()

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
    app.debug = True
    if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        scheduler = BackgroundScheduler()
        scheduler.start()
        scheduler.add_job(
            func=update_all,
            trigger=IntervalTrigger(seconds=update_interval),
            id='cage_update_job',
            name='trigger cage update',
            replace_existing=True)
        # Shut down the scheduler when exiting the app
        atexit.register(lambda: scheduler.shutdown())
    app.run(host='0.0.0.0', port=80)

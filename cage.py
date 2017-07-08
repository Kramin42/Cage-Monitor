import logging
import time

from Adafruit_DHT import read_retry
import RPi.GPIO as GPIO

class Cage:
    def __init__(self, name, sensor_chan, lamp_pin, pump_pin,
             temp_goal, temp_prec, hum_threshold):
        self.name = name
        self.sensor_chan = sensor_chan
        self.lamp_pin = lamp_pin
        self.pump_pin = pump_pin
        self.temp_goal = temp_goal
        self.temp_prec = temp_prec
        self.hum_threshold = hum_threshold
        self.lamp_on = False
        self.lamp_auto = True
        self.pump_on = False
        self.pump_auto = False
        self.temp = None
        self.hum = None
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(lamp_pin, GPIO.OUT, initial=self.lamp_on)
        GPIO.setup(pump_pin, GPIO.OUT, initial=self.pump_on)
    
    def read_sensor(self):
        logging.debug('Reading {} sensor'.format(self.name))
        self.hum, self.temp = read_retry(22, self.sensor_chan)
        if self.hum != None and self.temp != None:
            logging.debug('{0}: Temp={1:0.1f}*  Humidity={2:0.1f}%'.format(
                self.name, self.temp, self.hum))
            return True
        else:
            logging.error('Failed to get temperature/humidity '
                          'for cage {}'.format(self.name))
            return False
    
    def setLamp(self, state):
        logging.debug('Turning {} lamp {}'.format(self.name,
                                                   'On' if state else 'Off'))
        self.lamp_on = state
        GPIO.output(self.lamp_pin, state)
    
    def pulsePump(self):
        logging.debug('Pulsing {} pump'.format(self.name))
        # pump for 1 sec
        GPIO.output(self.pump_pin, True)
        time.sleep(1)
        GPIO.output(self.pump_pin, False)
    
    def check_and_update(self):
        if read_sensor():
            if self.lamp_auto:
                if self.lamp_on and \
                   self.temp > self.temp_goal+self.temp_prec:
                    self.setLamp(False)
                elif not self.lamp_on and \
                     self.temp < self.temp_goal-self.temp_prec:
                    self.setLamp(True)
            if self.pump_auto:
                # pump if below threshold and if it didn't pump
                # last check, maybe use a countdown instead of just
                # a toggling boolean
                if not self.pump_on and self.hum < self.hum_threshold:
                    self.pulsePump()
                else:
                    self.pump_on = False


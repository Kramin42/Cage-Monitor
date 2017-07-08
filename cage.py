import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Cage:
    def __init__(self, name, sensor_chan, lamp_pin, pump_pin,
             temp_goal, temp_prec, hum_goal, hum_prec):
        self.name = name
        self.sensor_chan = sensor_chan
        self.lamp_pin = lamp_pin
        self.pump_pin = pump_pin
        self.temp_goal = temp_goal
        self.temp_prec = temp_prec
        self.hum_goal = hum_goal
        self.hum_prec = hum_prec
        self.lamp_on = False
        self.pump_on = False
    
    def checkAndUpdate(self):
        humidity, temperature = read_retry(22, self.sensor_chan)
        logger.debug('{}: Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(
            name, temperature, humidity))
        if self.lamp_on and \
           temperature > self.temp_goal+self.temp_prec:
            logger.debug('turning {} lamp off'.format(name))
            lamp_on = False
            GPIO.output(lamp_channel, False)
        elif not self.lamp_on and \
             temperature < self.temp_goal-self.temp_prec:
            logger.debug('turning {} lamp on'.format(name))
            lamp_on = True
            GPIO.output(lamp_channel, True)


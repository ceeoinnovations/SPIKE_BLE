import time
import distance_sensor as ds
import port,motor
import color_sensor as cs
from ble_midi import *

p = port.PORTA
m = port.PORTE

fred = midi('Mary')

while True:
    d = ds.get_distance(p)
    sensor = int((d-40)/15+48)
    pos = motor.motor_get_absolute_position(m)
    speed = abs(pos)/360
    if fred.connected():
        fred.NewNote(sensor)
    time.sleep(speed)

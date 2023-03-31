import distance_sensor as ds
import port,time

p1 = port.PORTD

# Get distance from object of distance sensor connected to port A
while True:
    d = ds.get_distance(p1)
    n=int((d-40)/10+48)
    print(n)
    time.sleep(0.1)

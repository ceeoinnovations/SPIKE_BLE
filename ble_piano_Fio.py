import struct
import ble_CBR
import bluetooth
import button
import time
import distance_sensor as ds
import port,time

p1 = port.PORTD
p2 = port.PORTF

NoteOn = 0x90
NoteOff = 0x80
MaxVol = 127
MinVol = 0

done = lambda : button.button_pressed(button.BUTTON_RIGHT)

package = [0x00,0x00,0x00,0x00,0x00]

def note(cmd,value,volume):
    timestamp_ms = time.ticks_ms()
    package[0] = (timestamp_ms >> 7 & 0b111111) | 0x80
    package[1] =  0x80 | (timestamp_ms & 0b1111111)
    package[2] =  0x80 | cmd
    package[3] = value
    package[4] = volume
    return struct.pack("bbbbb", package[0], package[1], package[2], package[3], package[4])

def Piano():
    ble = bluetooth.BLE()
    p = ble_CBR.BLESimplePeripheral(ble, 'MIDI', 'MySpike')

    def on_rx(v):
        print("RX", v)
    
    p.on_write(on_rx)
        
    old_n = 0
    old_m = 0
    m=0
    n=0
    while not done():
        if p.is_connected():
                d = ds.get_distance(p1)
                d2 = ds.get_distance(p2)
                if d < 0:
                    p.send(note(NoteOff,old_n,MinVol))
                    old_n = 0
                else:
                    n=int((d-40)/15+48)
                    if n != old_n:
                        p.send(note(NoteOff,old_n,MinVol))
                        p.send(note(NoteOn,n,MaxVol))
                        old_n = n
                if d2 < 0:
                    p.send(note(NoteOff,old_m,MinVol))
                    old_m = 0
                else:
                    m = int((d2-40)/15+48)
                    if m != old_m:
                        p.send(note(NoteOff,old_m,MinVol))
                        p.send(note(NoteOn,m,MaxVol))
                        old_m = m
                print(d, n, d2, m)
                time.sleep(0.1)
    
Piano()

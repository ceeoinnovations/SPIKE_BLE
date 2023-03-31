'''
Micro Python Midi
This module implements channel commands according to the midi specification.
Each midi message consists of 3 bytes.
The first byte is the sum of the command and the midi channel (1-16 > 0-F).
the value of bytes 2 and 3 (data 1 and 2) are dependant on the command.
command     data1                   data2                  Description
-------     -----                   -----                  -----------
0x80-0x8F   Key # (0-127)           Off Velocity (0-127)   Note Off
0x90-0x90   Key # (0-127)           On Velocity (0-127)    Note On
0xA0-0xA0   Key # (0-127)           Pressure (0-127)       Poly Pressure
0xB0-0xB0   Control # (0-127)       Control Value (0-127)  Control
0xC0-0xC0   Program # (0-127)       Not Used (send 0)      Program Change
0xD0-0xD0   Pressure Value (0-127)  Not Used (send 0)      Channel Pressure
0xE0-0xE0   Range LSB (0-127)       Range MSB (0-127)      Pitch Bend
http://www.midi.org/techspecs/midimessages.php
'''

import struct
import ble_CBR
import bluetooth
import button
import time
import distance_sensor as ds
import port,time
import color_sensor as cs

done = lambda : button.button_pressed(button.BUTTON_RIGHT)

package = [0x00,0x00,0x00,0x00,0x00]

class midi:
    def __init__(self, name = 'MySpike'):
        n = name[0:7]
        self.connection = ble_CBR.BLESimplePeripheral(bluetooth.BLE(), 'MIDI', n)
        self.connection.on_write(self.on_receive)
        self.buffer = []
        
    def on_receive(self, msg):
        print("RX: ", msg)
      
    def connected(self):
        return self.connection.is_connected()

    def convert(self, cmd, value, volume):
        timestamp_ms = time.ticks_ms()
        package[0] = (timestamp_ms >> 7 & 0b111111) | 0x80
        package[1] =  0x80 | (timestamp_ms & 0b1111111)
        package[2] =  0x80 | cmd
        package[3] = value
        package[4] = volume
        return struct.pack("bbbbb", package[0], package[1], package[2], package[3], package[4])

    def NoteOn(self, note = 40, volume = 127):  
        if self.connected():
            self.connection.send(self.convert(0x90,note,volume))
            self.buffer.insert(0,note)  # put in front
        else:
            print('not connected')
            
    def NoteOff(self, note = 40):
        if self.connected():
            self.connection.send(self.convert(0x80,note,0))
            try:
                self.buffer.remove(note)
            except:
                pass
        
    def NewNote(self, note = 40, volume = 127):
        self.AllOff()
        self.NoteOn(note,volume)
        
    def AllOff(self):
        for note in self.buffer:
            self.NoteOff(note) 
        
    def test(self, duration = 1):
        notes = [60,61,62,63,64,63,62,61]
        for note in notes:
            self.NewNote(note)
            time.sleep(duration)
        self.AllOff()
        
    def close(self):
        self.AllOff()
        self.connection.disconnect()
    
'''
p1 = port.PORTD
p2 = port.PORTF
light = port.PORTA
    
fred = midi('ChrisSPIKE')

while not done:
    d = ds.get_distance(p)
    cs.get_color(light)]
    cs.get_reflection(light)
    if fred.connected():
        fred.NewNote((d-40)/15+48)
fred.close()
'''

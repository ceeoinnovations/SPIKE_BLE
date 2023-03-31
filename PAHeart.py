import struct
import ble_CBR
import bluetooth
import button
import time
import color_sensor
import port
import motor

light = port.PORTA
p1=port.PORTE
speed = 1000

# Get color - see Defines.py for the list of colors
colors = {
    -1:'ERR',
    0:"LEGO_BLACK",
    1:"LEGO_MAGENTA",
    2:"LEGO_PURPLE",
    3:"LEGO_BLUE",
    4:"LEGO_AZURE",
    5:"LEGO_TURQUOISE",
    6:"LEGO_GREEN",
    7:"LEGO_YELLOW",
    8:"LEGO_ORANGE",
    9:"LEGO_RED",
    10:"LEGO_WHITE",
    11:"LEGO_DIM_WHITE",
    }

notes = [69,67,64]  # B Y  R

NoteOn = 0x90
NoteOff = 0x80
MaxVol = 127
MinVol = 0

done = lambda : button.button_isPressed(button.BUTTON_RIGHT)[0]
faster = lambda : button.button_isPressed(button.BUTTON_LEFT)[0]

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
    p = ble_CBR.BLESimplePeripheral(ble, 'MIDI', 'MySPIKE')

    def on_rx(v):
        print("RX", v)
    
    p.on_write(on_rx)
        
    was_connected = False
    
    while not done():
        if p.is_connected():
            for x in notes:
                p.send(note(NoteOn,x,MaxVol))
                time.sleep(0.5)
                p.send(note(NoteOff,x,MinVol))
                time.sleep(0.5)
            #was_connected = True
        else:
            if was_connected:
                break
        time.sleep_ms(1000)
    
#Piano()

def fred():
    ble = bluetooth.BLE()
    p = ble_CBR.BLESimplePeripheral(ble, 'MIDI', 'MySPIKE')

    def on_rx(v):
        print("RX", v)
    
    p.on_write(on_rx)
        
    was_connected = False
    speed = 3000
    motor.motor_move_at_speed(p1, speed)
    while not done():
        #if button.button_isPressed(button.BUTTON_LEFT)[0]:
         #   speed = speed + 100
         #   motor.motor_move_at_speed(p1, speed)
        reply = colors[color_sensor.get_color(light)]
        #time.sleep(0.1)
        if reply == 'ERR':
            continue
        x = 64 if reply == 'LEGO_RED' else 67 if reply =='LEGO_YELLOW' else 69
        #print(reply)
        if p.is_connected():
            print(x)
            p.send(note(NoteOn,x,MaxVol))
            time.sleep(0.5)
            p.send(note(NoteOff,x,MinVol))
fred()
    


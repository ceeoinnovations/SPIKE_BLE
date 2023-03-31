import button
import time
from ble_MIDI import *

notes = [60,61,62,63,64,63,62,61]

done = lambda : button.button_pressed(button.BUTTON_RIGHT)
    
def Music():
    midi = MIDI_Player('chris')
    midi.wait_for_connection()
    Piano = MIDI_Instrument(midi, instruments['Acoustic Grand Piano'],channel = 0)
    Trumpet = MIDI_Instrument(midi, instruments['Trumpet'],channel = 1)
    
    try:
        while not done():
            for x in notes:
                Trumpet.on(x,velocity['ff'])
                Piano.on(x,velocity['ff'])
                time.sleep(0.5)
                Trumpet.off(x)
                Piano.off(x)
                time.sleep(0.5)
    except:
        pass
        
    midi.disconnect()

Music()



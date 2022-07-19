# This example demonstrates a UART periperhal.

import bluetooth
import ble_CBR
import time

def Joy():
    ble = bluetooth.BLE()
    p = ble_CBR.BLESimplePeripheral(ble, 'UART', 'joystick')

    def on_rx(v):
        print("RX", v)

    p.on_write(on_rx)
    
    was_connected = False

    i = 0
    while True:
        if p.is_connected():
            # Short burst of queued notifications.
            for _ in range(3):
                data = str(i) + "_"
                print("TX", data)
                p.send(data)
                i += 1
            was_connected = True
        else:
            if was_connected:
                break
        time.sleep_ms(1000)

Joy()

# This is from Damien's example - running the UART Central

import bluetooth
import time
import button
import ble_CBR

def Car():
    ble = bluetooth.BLE()
    central = ble_CBR.BLESimpleCentral(ble)

    not_found = False

    def on_scan(addr_type, addr, name):
        if addr_type is not None:
            print("Found peripheral:", addr_type, addr, name)
            central.connect()
        else:
            nonlocal not_found
            not_found = True
            print("No peripheral found.")

    central.scan(callback=on_scan)

    # Wait for connection...
    while not central.is_connected():
        time.sleep_ms(100)
        if not_found:
            return

    print("Connected")

    def on_rx(v):
        print("RX", str(bytes(v)))

    central.on_notify(on_rx)

    with_response = False
    done = lambda : button.button_isPressed(button.BUTTON_RIGHT)[0]

    i = 0
    while central.is_connected() and not done():
        try:
            v = str(i) + "_"
            print("TX", v)
            central.write(v, with_response)
        except:
            print("TX failed")
        i += 1
        time.sleep_ms(4000 if with_response else 1000)
    central.disconnect()
    central.scan(callback = None )
    print("Disconnected")

Car()

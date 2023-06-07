import math
import time

from frame_processing_module import *
from usb_module import *

# --------------------------------------------------------- INPUT PARAMS
SIGNAL_TYPE = "SIN"
# SIGNAL_TYPE = "SQUARE"

# SIN params
F_SIGNAL_SIN = 0.1  # [Hz] - SIN signal freq
AMP_SIN = 30  # [deg] - SIN signal amplitude

# SQUARE params
F_SIGNAL_SQUARE = 0.25  # [Hz] - SQUARE signal freq
AMP_SQUARE = 30  # [deg] - SQUARE signal amplitude


# --------------------------------------------------------- MAIN PROGRAM
F_TX = 20  # [Hz] - system transmission freq
if SIGNAL_TYPE == "SIN":
    F_SIGNAL = F_SIGNAL_SIN
    AMP = AMP_SIN
elif SIGNAL_TYPE == "SQUARE":
    F_SIGNAL = F_SIGNAL_SQUARE
    AMP = AMP_SQUARE
else:
    print("Wrong signal type")
    quit()

T_SIGNAL = 1 / F_SIGNAL  # [s] -  system transmission period
T_SYSTEM = 1 / F_TX  # [s] - signal discret period

start_time = 0  # [s] loop start time
samples_cnt = 0
time_window = 0  # [s] for square wave generation only
angle = 0  # [deg]


with serial.Serial(**USB_PARAMS) as ser:
    # Port search
    ser.port = usb_port_search()

    # Port open
    if not (usb_port_open(ser)):
        quit()

    print("\nGeneration start")
    print("Signal frequency: {0}\nSystem frequency: {1}\n\n".format(F_SIGNAL, F_TX))

    # Main loop
    while True:
        # Loop time calc
        current_time = time.time()
        delta_time = current_time - start_time

        # Angle calculation
        if delta_time >= T_SYSTEM:
            start_time = current_time
            if SIGNAL_TYPE == "SIN":
                angle = AMP * math.sin(2 * math.pi * F_SIGNAL / F_TX * samples_cnt)
            elif SIGNAL_TYPE == "SQUARE":
                if time_window >= (T_SIGNAL / 2):
                    # Change signal state
                    angle = -1 * angle + AMP
                    time_window = 0

            # Message formation
            data = frame_generation(angle)

            # Message transmit
            if ser.is_open == True:
                try:
                    ser.write(data)
                    print(
                        "Angle: {0:3.3f}, Message: {1}, Sample: {2}, Time: {3:4.2f}s".format(
                            angle, data.hex(), samples_cnt, (T_SYSTEM * samples_cnt)
                        )
                    )
                except:
                    ser.close()
            else:
                # Connection lost
                print("Connection lost! Trying to reconnect...")
                usb_port_open(ser)

            time_window += T_SYSTEM
            samples_cnt += 1

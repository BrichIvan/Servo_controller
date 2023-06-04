import math
import time

from usb_module import *

# --------------------------------------------------------- INPUT PARAMS
SIGNAL_TYPE = "SIN"
# SIGNAL_TYPE = "SQUARE"
SERVO_ANGLE_MAX = 90
INT16_MAX_VALUE = 32767

f_tx = 20  # [Hz] - system transmission freq
f_signal = 0.1  # [Hz] - signal discret freq
amp = 50  # [deg] - signal amplitude

t_signal = 1 / f_signal  # [s] -  system transmission period
t_system = 1 / f_tx  # [s] - signal discret period

start_time = 0  # [s]
samples_cnt = 0
time_window = 0  # [s] for square wave generation only
angle = 0  # [deg]


# CRC32-MPEG2 calculation
def crc32_mpeg2(buf, crc=0xFFFFFFFF):
    for val in buf:
        crc ^= val << 24
        for _ in range(8):
            crc = crc << 1 if (crc & 0x80000000) == 0 else (crc << 1) ^ 0x104C11DB7
    return crc


# Angle transmission
def angle_transmit(angle):
    angle = int(
        angle * (INT16_MAX_VALUE / SERVO_ANGLE_MAX)
    )  # Scale and transform to int
    angle_bytes = angle.to_bytes(
        length=2, byteorder="big", signed=True
    )  # transform to bytes

    if angle < 0:
        crc32_value = crc32_mpeg2(b"\xFF\xFF" + angle_bytes)
    else:
        crc32_value = crc32_mpeg2(b"\x00\x00" + angle_bytes)

    crc32_bytes = int.to_bytes(crc32_value, length=4, byteorder="big", signed=False)

    data = angle_bytes + crc32_bytes

    # print ("\nInput data in hex: {0}".format(angle_bytes.hex()))
    # print ("CRC32-MPEG2 hex: {0}".format(CRC32_bytes.hex()))
    # print ("Full message: {0}\n".format(data.hex()))
    return data


with serial.Serial(**USB_PARAMS) as ser:
    # Port setup
    ser.port = usb_port_search()
    if not (usb_port_open(ser)):
        quit()

    print("\nGeneration start")
    print("Signal frequency: {0}\nSystem frequency: {1}\n\n".format(f_signal, f_tx))

    while True:
        current_time = time.time()
        delta_time = current_time - start_time
        if delta_time >= t_system:
            start_time = current_time
            if SIGNAL_TYPE == "SIN":
                angle = amp * math.sin(
                    2 * math.pi * f_signal / f_tx * samples_cnt
                )  # float
            elif SIGNAL_TYPE == "SQUARE":
                if time_window >= t_signal:
                    # Change signal state
                    angle = -1 * angle + amp
                    time_window = 0
            else:
                print("Wrong signal type")
                quit()

            # MESSAGE FORMATION
            data = angle_transmit(angle)

            if ser.is_open == True:
                try:
                    ser.write(data)
                    print(
                        "Angle: {0:3.3f}, Message: {1}, Sample: {2}, Time: {3:4.2f}s".format(
                            angle, data.hex(), samples_cnt, (t_system * samples_cnt)
                        )
                    )
                except:
                    ser.close()
            else:
                # connection lost
                print("Connection lost! Trying to reconnect...")
                usb_port_open(ser)

            time_window += t_system
            samples_cnt += 1

import time
import math
import serial

# CRC32-MPEG2 calculation
def crc32mpeg2(buf, crc=0xFFFFFFFF):
    for val in buf:
        crc ^= val << 24
        for _ in range(8):
            crc = crc << 1 if (crc & 0x80000000) == 0 else (crc << 1) ^ 0x104c11db7
    return crc

# Angle transmission
def AngleTransmit (angle):
    angle = int(angle * (INT16_MAX_VALUE/SERVO_ANGLE_MAX)) # Scale and transform to int
    angle_bytes = angle.to_bytes (length=2, byteorder="big", signed=True) # transform to bytes

    CRC32 = crc32mpeg2 (b'\x00\x00' + angle_bytes)
    CRC32_bytes = int.to_bytes (CRC32, length=4, byteorder="big", signed=False)

    data = angle_bytes + CRC32_bytes

    # print ("\nInput data in hex: {0}".format(angle_bytes.hex()))
    # print ("CRC32-MPEG2 hex: {0}".format(CRC32_bytes.hex()))
    # print ("Full message: {0}\n".format(data.hex()))
    return data


#--------------------------------------------------------- INPUT PARAMS
f_tx = 20 # [Hz] - system transmission freq
f_signal = 0.2 # [Hz] - signal discret freq
amp = 60 # [deg] - sin amp

t_signal = 1/f_signal # [s] -  system transmission period
t_system = 1/f_tx # [s] - signal discret period
samples_qty = t_signal / t_system # Number of samples per signal period

SERVO_ANGLE_MAX = 90
INT16_MAX_VALUE = 32767

COM_BAUDRATE = 115200
COM_PORT = "COM10"
TIMEOUT = 1

start_time = time.time() - 2*t_system # [s]
samples_cnt = 0
angle = 0 # [deg]


with serial.Serial() as ser:
    # Port setup
    ser.port = COM_PORT
    ser.baudrate = COM_BAUDRATE
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.bytesize = serial.EIGHTBITS
    ser.timeout = None

    # Port open
    try:
        ser.open()
    except serial.SerialException:
        print("Не удалось установить соединение")
        print("Проверьте подключение контроллера")
        quit()

    ser.reset_input_buffer()

    print("connected to: " + ser.portstr)

    print ("\nGeneration start")
    print ("Signal frequency: {0}\nSystem frequency: {1}\n\n".format(f_signal, f_tx))

    while True:
        current_time = time.time()
        delta_time = current_time - start_time
        if (delta_time > t_system):
            # print (ser.readline())
            start_time = current_time
            angle = amp * math.sin (2*math.pi * f_signal/f_tx * samples_cnt) # float
            
            # MESSAGE FORMATION
            data = AngleTransmit (angle)
            ser.write (data)

            print ("Angle: {0:3.3f}, Message: {1}, Sample: {2}, Time: {3:4.2f}s".format(angle, data.hex(), samples_cnt, (t_system*samples_cnt)))
            samples_cnt += 1
import serial
from serial.tools.list_ports import comports

# COM_PORT = "COM10"
STM_VID = 1155
STM_PID_FS = 22336

USB_PARAMS = {
    "baudrate": 115200,
    "stopbits": serial.STOPBITS_ONE,
    "parity": serial.PARITY_NONE,
    "bytesize": serial.EIGHTBITS,
    "timeout": None,
}

stm_port = []


# COM port search
def usb_port_search():
    ports = comports()
    for i in range(len(ports)):
        if ports[i].vid == STM_VID:
            stm_port.append(ports[i].name)

    if len(stm_port) == 0:
        raise RuntimeError(f"No STM controller")
    elif len(stm_port) == 1:
        print("STM controller detected. COM port: {0}".format(stm_port[0]))
        return stm_port[0]
    else:
        raise RuntimeError(
            f"Обнаружено более одного контроллера сервопривода STM: {0}".format(
                stm_port[:]
            )
        )


# USB port connection
def usb_port_open(ser):
    if not (isinstance(ser, serial.Serial)):
        raise TypeError("Wrong serial class")

    # Port open
    try:
        ser.open()
        ser.reset_input_buffer()
        print("Connected to: " + ser.portstr)
        return True
    except serial.SerialException:
        print("Connection failed")
        print("Check controller connection")
        return False

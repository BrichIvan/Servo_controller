SERVO_ANGLE_MAX = 90
INT16_MAX_VALUE = 32767


# CRC32-MPEG2 calculation
def crc32_mpeg2(buf, crc=0xFFFFFFFF):
    for val in buf:
        crc ^= val << 24
        for _ in range(8):
            crc = crc << 1 if (crc & 0x80000000) == 0 else (crc << 1) ^ 0x104C11DB7
    return crc


# message packing
def frame_generation(angle):
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

    return data

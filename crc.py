# Функция вычисления контрольной суммы crc8.
def crc8(data):
    crc = 0xFF
    polynomial = 0x31  # Полином для CRC-8 (CRC-8-ATM)

    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ polynomial
            else:
                crc <<= 1
            crc &= 0xFF

    return crc.to_bytes(1, byteorder='big')


# Функция вычисления контрольной суммы crc16.
def crc16(data):
    crc = 0xFFFF
    polynomial = 0x1021  # Полином для CRC-16 (CRC-16-IBM)

    for byte in data:
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ polynomial
            else:
                crc <<= 1
            crc &= 0xFFFF

    return crc.to_bytes(2, byteorder='big')

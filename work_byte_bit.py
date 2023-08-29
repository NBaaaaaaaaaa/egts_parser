# Функция перевода из 16 системы в 10.
def hex_to_dec(byte):
    if not byte:
        return None

    return int.from_bytes(byte, byteorder='big')


# Функция возвращает значение байта.
def param_byte(packet, count, reverse=True):
    param = packet[:count]
    packet = packet[count:]

    if count > 1 and reverse:
        param = param[::-1]

    return packet, param


# Функция получения битов из байта.
def param_bit(byte, cart):
    decimal_number = hex_to_dec(byte)
    binary_string = bin(decimal_number)[2:].zfill(sum(cart))
    packet = list(binary_string)
    tup = list()
    for i in cart:
        tup.append(''.join(packet[:i]))
        packet = packet[i:]
    return tup


# Функция получения строки из последовательности байтов.
def get_string(byte_string):
    info_str = splitter = b''
    for byte in byte_string:
        if byte != 0:
            info_str += byte.to_bytes(1, byteorder='big')

        else:
            splitter += byte.to_bytes(1, byteorder='big')
            break

    return byte_string[:len(info_str + splitter)], str(info_str)[2:-1], splitter

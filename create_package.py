from crc import crc8, crc16
from lists.sfrd_types import Sfrd_types
from work_byte_bit import hex_to_dec


# Функция создания поля SFRD и SFRCS для подтверждения пакета Транспортного Уровня.
def create_EGTS_PT_RESPONSE(rpid, pr):
    rpid = rpid[::-1]
    pr = pr.to_bytes(1, byteorder='big')

    return rpid + pr + crc16(rpid + pr)[::-1]
    # Структуры  SDR 1, ... не добавил. Хз надо или нет.


# Функция создания ответного пакета. Пока None второй аргумент, позже будет нужен.
def create_response_package(dict_data, package_type, code):
    # print("Пакет с кодом {code}".format(code=code))
    send_package = b''

    for param in ['PRV', 'SKID', 'tmp_byte', 'HL', 'HE', 'FDL', 'PID', 'PT', 'HCS']:
        if param in ("FDL", ):
            send_package += int(3).to_bytes(2, byteorder='little')

        elif param in ("PT", ):
            send_package += package_type.to_bytes(1, byteorder='little')

        elif param in ("PRA", "RCA", "PID"):
            send_package += dict_data[param][::-1]

        elif param in ("HCS", ):
            send_package += crc8(send_package)

        else:
            send_package += dict_data[param]

    # Формирование полей sfrd и sfrcs.
    if package_type == Sfrd_types.EGTS_PT_RESPONSE.value:
            #  EGTS_PT_RESPONSE (подтверждение на пакет транспортного уровня);
            send_package += create_EGTS_PT_RESPONSE(dict_data["PID"], code)

        # пока не используется
    elif package_type == Sfrd_types.EGTS_PT_APPDATA.value | Sfrd_types.EGTS_PT_SIGNED_APPDATA.value:
        # EGTS_PT_APPDATA (пакет, содержащий данные протокола уровня поддержки услуг);
        # EGTS_PT_SIGNED_APPDATA (пакет, содержащий данные протокола уровня поддержки услуг с цифровой подписью).
        # send_package += dict_data["SFRD"] + dict_data["SFRCS"][::-1]
        pass

    else:
        print("Неизвестный тип пакета.")

    # print(f"Пакет на отправку: {send_package}\n")
    return send_package

from enum import Enum


# Коды результатов обработки.
class Codes(Enum):
    EGTS_PC_OK = 0	                    # успешно обработано
    EGTS_PC_IN_PROGRESS = 1	            # в процессе обработки (результат обработки ещё не известен)
    EGTS_PC_UNS_PROTOCOL = 128	        # неподдерживаемый протокол
    EGTS_PC_DECRYPT_ERROR = 129	        # ошибка декодирования
    EGTS_PC_PROC_DENIED = 130	        # обработка запрещена
    EGTS_PC_INC_HEADERFORM = 131	    # неверный формат заголовка
    EGTS_PC_INC_DATAFORM = 132	        # неверный формат данных
    EGTS_PC_UNS_TYPE = 133	            # неподдерживаемый тип
    EGTS_PC_NOTEN_PARAMS = 134	        # неверное количество параметров
    EGTS_PC_DBL_PROC = 135	            # попытка повторной обработки
    EGTS_PC_PROC_SRC_DENIED = 136	    # обработка данных от источника запрещена
    EGTS_PC_HEADERCRC_ERROR = 137	    # ошибка контрольной суммы заголовка
    EGTS_PC_DATACRC_ERROR = 138	        # ошибка контрольной суммы данных
    EGTS_PC_INVDATALEN = 139	        # некорректная длина данных
    EGTS_PC_ROUTE_NFOUND = 140	        # маршрут не найден
    EGTS_PC_ROUTE_CLOSED = 141	        # Маршрут закрыт
    EGTS_PC_ROUTE_DENIED = 142    	    # маршрутизация запрещена
    EGTS_PC_INVADDR = 143	            # неверный адрес
    EGTS_PC_TTLEXPIRED = 144	        # превышено количество ретрансляции данных
    EGTS_PC_NO_ACK = 145	            # нет подтверждения
    EGTS_PC_OBJ_NFOUND = 146	        # объект не найден
    EGTS_PC_EVNT_NFOUND = 147	        # событие не найдено
    EGTS_PC_SRVC_NFOUND = 148	        # сервис не найден
    EGTS_PC_SRVC_DENIED = 149	        # сервис запрещён
    EGTS_PC_SRVC_UNKN = 150	            # неизвестный тип сервиса
    EGTS_PC_AUTH_DENIED = 151	        # авторизация запрещена
    EGTS_PC_ALREADY_EXISTS = 152	    # объект уже существует
    EGTS_PC_ID_NFOUND = 153	            # идентификатор не найден
    EGTS_PC_INC_DATETIME = 154	        # неправильная дата и время
    EGTS_PC_IO_ERROR = 155	            # ошибка ввода/вывода
    EGTS_PC_NO_RES_AVAIL = 156	        # недостаточно ресурсов
    EGTS_PC_MODULE_FAULT = 157	        # внутренний сбой модуля
    EGTS_PC_MODULE_PWR_FLT = 158	    # сбой в работе цепи питания модуля
    EGTS_PC_MODULE_PROC_FLT = 159	    # сбой в работе микроконтроллера модуля
    EGTS_PC_MODULE_SW_FLT = 160     	# сбой в работе программы модуля
    EGTS_PC_MODULE_FW_FLT = 161	        # сбой в работе внутреннего ПО модуля
    EGTS_PC_MODULE_IO_FLT = 162	        # сбой в работе блока ввода/вывода модуля
    EGTS_PC_MODULE_MEM_FLT = 163	    # сбой в работе внутренней памяти модуля
    EGTS_PC_TEST_FAILED = 164	        # тест не пройден


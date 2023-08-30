import multiprocessing
import socket
from processing_package import package_data_processing
from threading import Thread

from work_db import connect_main_db, Packet_data, create_check_connect, create_cursor, connect_proc_loc_db, \
                    create_local_cursor, create_th_save_data

from logger_files.logger import Logging
from logger_files.type_text import Types_text

from config import queue_length, devices_count
from datetime import datetime
import time


# Процедура получения и отправки пакетов.
def receive_data(data, connection, data_for_db, logging):
    try:
        # print("Получены данные:", data)
        print("Пакет получен: {d} - {data}".format(d=datetime.now().time().strftime('%H:%M:%S'), data=data))
        logging.logging(fromm=1, to=2, type_text=Types_text.SENT_DATA.value, text=data)

        packet = package_data_processing(data, data_for_db, logging)
        connection.send(packet)
        print("Отправлен пакет на пакет: {d} - {packet}".format(
            d=datetime.now().time().strftime('%H:%M:%S'), packet=packet))
        logging.logging(fromm=2, to=1, type_text=Types_text.SENT_DATA.value, text=packet)

    except KeyboardInterrupt:
        pass


# Процедура работы процесса.
def process_work(connection, address):
    try:
        # Создаем объект класса, для последующей записи данных в бд.
        data_for_db = Packet_data()
        create_cursor(connect_proc_loc_db())

        logging = Logging(address)
        logging.logging(fromm=1, to=2, type_text=Types_text.CONNECTED.value)

        while True:
            # Получаем данные от клиента
            data = connection.recv(1024)

            if not data:
                break

            # Создаем новый поток для обработки данных клиента
            t = Thread(target=receive_data, args=(data, connection, data_for_db, logging))
            t.start()

        logging.logging(fromm=1, to=2, type_text=Types_text.DISCONNECTED.value)
        # Закрываем соединение.
        connection.close()

    except Exception as e:
        print(e)
        

# Процедура работы сервера.
def server_work():
    process_list = []

    # Процедура проверки живых процессов.
    def check_process_count():
        while True:
            for pr in process_list:
                if not pr.is_alive():
                    process_list.remove(pr)

            time.sleep(3)

    # Создаем подключение к бд.
    create_cursor(connect_main_db())
    # Создаем подключение к локальной бд процессов.
    create_local_cursor(connect_proc_loc_db())

    # Создаем поток проверки подключения к удаленной бд.
    create_check_connect()
    # Создаем поток сохранения данных в серверную бд.
    create_th_save_data()

    port = 1337

    # Создаем сокет для прослушивания порта
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(queue_length)

    print("Сервер запущен и слушает порт {}...".format(port))

    # Создаем новый поток для проверки живих процессов.
    t = Thread(target=check_process_count)
    t.start()

    try:
        while True:
            if len(process_list) <= devices_count:
                # Принимаем входящее соединение
                connection, address = server_socket.accept()
                print("Установлено соединение с {}".format(address))

                process = multiprocessing.Process(target=process_work, args=(connection, address))
                process.start()
                process_list.append(process)

    except KeyboardInterrupt as e:
        pass

    # Вот с этим надо разобарться как закрыть подулючение
    # Закрываем соединение с бд.
    Packet_data.db_connection.close()
    Packet_data.loc_db_connection.close()
    # Закрываем сокет.
    server_socket.close()


# Блок кода для тестов.
if __name__ == "__main__":
    # Раскомментить строку.
    server_work()

import time

import mysql.connector
import sqlite3

from datetime import datetime

from config import host, port, user, password, db_name, l_db_name, table_name, time_sleep, l_pr_db_name

from logger_files.type_text import Types_text
from logger_files.logger import Logging

from threading import Thread


# Функция подключения к локальной бд для сохранения данных с процесса.
def connect_proc_loc_db():
    # Подключение к существующей базе данных или создание новой, если её нет.
    connection = sqlite3.connect('local_db/{name}.db'.format(name=l_pr_db_name), check_same_thread=False)
    return {"main": False, "connection": connection}


# Функция подключения к локальной бд.
def connect_local_db():
    # Подключение к существующей базе данных или создание новой, если её нет.
    connection = sqlite3.connect('local_db/{name}.db'.format(name=l_db_name), check_same_thread=False)
    return connection


# Функция подключения к основной бд.
def connect_main_db():
    try:
        # Подключаемся к бд.
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            ssl_disabled=True
        )

        return {"main": True, "connection": connection}

    except Exception as e:
        print(e)
        Logging("").logging(fromm=2, to=3, type_text=Types_text.ERROR.value,
                            text="Ошибка подключения к серверу с бд. {e}".format(e=e))
        return {"main": False, "connection": connect_local_db()}


# Процедура сохранения подключения к удаленной бд.
def create_cursor(db_connection):
    Packet_data.is_main = db_connection["main"]
    Packet_data.db_connection = db_connection["connection"]
    Packet_data.cursor = Packet_data.db_connection.cursor()


# Процедура сохранения подключения к локальной бд с данными процессов.
def create_local_cursor(db_connection):
    Packet_data.loc_db_connection = db_connection["connection"]
    Packet_data.loc_cursor = Packet_data.loc_db_connection.cursor()


# Процедура проверки доступа к серверу с бд.
def check_connect():
    while True:
        if not Packet_data.is_main:
            # Создаем подключение к бд. Если идет запись в локальную бд.
            create_cursor(connect_main_db())

        time.sleep(time_sleep)


# Процедура создания потока проверки доступа к серверу с бд.
def create_check_connect():
    # Создаем новый поток для обработки данных клиента
    t = Thread(target=check_connect, daemon=True)
    t.start()


# Процедура сохранения данных пакета в осн бд.
def th_save_data():
    while True:
        Packet_data.gts_put()

        time.sleep(5)


# Процедура создания потока сохранения данных в серверную бд.
def create_th_save_data():
    # Создаем новый поток для сохранения данных с локальной бд процессов в бд серверную.
    t = Thread(target=th_save_data, daemon=True)
    t.start()


# Процедура записи данных в локальную бд. По итогу можно сделать из этого процедуру в самой бд и избавиться от
# такого большого блока кода.
def insert_sqlite3(insert_data):
    try:
        type_placeholder = {
            True: "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",
            False: "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"
        }

        insert_query = '''
        INSERT INTO {table_name}
          (imei, terminal_id, rec_id, event_id, time_recv,
          time_event, lat, lon, coords_sign, speed, vector, height, is_valid,
          is_blackbox, point_source, fuel_level_1, fuel_level_2, fuel_level_3, fuel_level_4, sensors)
        VALUES ({ttype})
        '''.format(table_name=table_name, ttype=type_placeholder[Packet_data.is_main])

        Packet_data.cursor.execute(insert_query, insert_data)
        Packet_data.db_connection.commit()

    except Exception as e:
        print(e)


class Packet_data:
    tid = oid = evid = tm = lat = long = spd = dir = alt = vld = bb = src = 0
    imei = coords = sensors = ''
    llsd = []

    # Статические переменные.
    is_main = db_connection = cursor = in_local = None
    loc_db_connection = loc_cursor = None

    def update_auth(self, tid, imei):
        self.tid = tid
        self.imei = imei

    def set_oid(self, oid):
        self.oid = oid

    def set_evid(self, evid):
        self.evid = evid

    def set_tm(self, tm):
        self.tm = tm

    def update_pos_data(self, lat, long, lohs, lahs, bb, vld, spd, dir, src, alt):
        self.lat = round(lat * 90 / 4294967295, 3)
        self.long = round(long * 180 / 4294967295, 3)

        if lahs and lohs:
            self.coords = 'SE'

        elif lahs:
            self.coords = 'SW'

        elif lohs:
            self.coords = 'NE'

        else:
            self.coords = 'NW'

        self.bb = bb
        self.vld = vld
        self.spd = spd
        self.dir = dir
        self.src = src
        self.alt = alt

    def update_llsd(self, llsd):
        self.llsd.append(llsd)

    def reset_llsd(self):
        self.llsd = []

    def gts_data_save(self):
        # Если колво значений меньше 4, то заполняем -1.
        while len(self.llsd) < 4:
            self.llsd.append(0)

        insert_data = [self.imei, self.tid, self.oid, self.evid, datetime.now(),
                       self.tm, self.lat, self.long, self.coords, self.spd, self.dir, self.alt, self.vld,
                       self.bb, self.src, self.llsd[0], self.llsd[1], self.llsd[2], self.llsd[3], self.sensors]

        insert_sqlite3(insert_data)

    # Метод записи данных в бд.
    @staticmethod
    def insert_data(data=None):
        try:
            # Вставка в бд.
            if not data:
                Packet_data.loc_cursor.execute('SELECT * FROM {table_name}'.format(table_name=table_name))

                # Получение всех строк результата в виде списка кортежей.
                rows = Packet_data.loc_cursor.fetchall()

                # Запись всех строк из локальной бд в удаленную.
                for row in [list(row) for row in rows]:
                    # Если записалось в основную бд.
                    if Packet_data.insert_data(row[1:]):
                        # Удаляем запись из локальной бд.
                        Packet_data.loc_cursor.execute('DELETE FROM {table_name} WHERE id = {r}'.format(
                            table_name=table_name, r=row[0]))
                        Packet_data.loc_db_connection.commit()

            # Вставка в удаленную бд с локальной бд.
            else:
                insert_data = data

                a = time.time()

                if Packet_data.is_main:
                    Packet_data.cursor.callproc("gts_put_test", insert_data)
                    Packet_data.db_connection.commit()

                else:
                    insert_sqlite3(insert_data)

                b = time.time()
                print("  Запись точки: {s} секунд".format(s=round(b - a, 2)))

            return True

        except Exception as e:
            print(e)
        #     # Packet_data.cursor.close()
        #     # Packet_data.db_connection.close()
            return False

    # Метод вставки данных в бд.
    @staticmethod
    def gts_put():
        # Запись в удаленную бд.
        if Packet_data.is_main:
            main_connect = True
            # Если соединение было разорвано.
            if not Packet_data.insert_data():
                create_cursor({"main": False, "connection": connect_local_db()})
                Packet_data.insert_data()
                main_connect = False

            if main_connect:
                # Если были записаны данные в локальную бд.
                if Packet_data.in_local and Packet_data.is_main:
                    local_connection = connect_local_db()
                    local_cursor = local_connection.cursor()

                    local_cursor.execute('SELECT * FROM {table_name}'.format(table_name=table_name))

                    # Получение всех строк результата в виде списка кортежей.
                    rows = local_cursor.fetchall()

                    # Запись всех строк из локальной бд в удаленную.
                    for row in [list(row) for row in rows]:
                        # Если записалось в основную бд.
                        if Packet_data.insert_data(row[1:]):
                            # Удаляем запись из локальной бд.
                            local_cursor.execute('DELETE FROM {table_name} WHERE id = {r}'.format(
                                table_name=table_name, r=row[0]))
                            local_connection.commit()

                    local_cursor.execute('SELECT * FROM {table_name}'.format(table_name=table_name))
                    if len(local_cursor.fetchall()) > 0:
                        Packet_data.in_local = False

                    # Закрываем соединение с локальной бд.
                    local_cursor.close()
                    local_connection.close()

        # Запись в локальную бд.
        else:
            Packet_data.insert_data()
            Packet_data.in_local = True

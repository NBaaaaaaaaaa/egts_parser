import os
from datetime import datetime
from config import logs_path


# Процедура создания папки для хранения логов.
def create_directory():
    try:
        os.mkdir("logs")

    except Exception as e:
        print(e)


# Процедура создания директорий под логи.
def create_directories():
    log_file = "{file}.{num}.txt"
    # Получение текущей даты.
    current_datetime = datetime.now()
    path = "{path}/{y}/{m}/{d}/".format(
        path=logs_path, y=current_datetime.year, m=current_datetime.month, d=current_datetime.day
    )
    # Создание директорий.
    os.makedirs(path, exist_ok=True)

    # Создание имени логу.
    list_files = os.listdir(path)
    # Если файлов нет в директории.
    if len(list_files) == 0:
        log_file = log_file.format(file=current_datetime.strftime("%d-%m-%Y"), num=0)

    # Если файлы есть в директории.
    else:
        # Получаем последний созданный файл.
        last_file = list_files[-1]

        # Если вес его >= 48 Мб
        if round(int(os.stat(path + last_file).st_size) / 1024 / 1024, 2) >= 48:
            log_file = log_file.format(file=current_datetime.strftime("%d-%m-%Y"), num=int(last_file.split(".")[1]) + 1)

        # Если вес его < 48 Мб
        else:
            log_file = last_file

    return path + log_file, current_datetime


class Logging:
    participants = {
        1: None,
        2: "Server",
        3: ""
    }

    def __init__(self, ip):
        if ip:
            self.participants[1] = ip

    # Процедура логирования.
    def logging(self, fromm=None, to=None, type_text=None, text=None):
        path, current_datetime = create_directories()

        messages = {
            1: "Подключился",
            2: "Отключился",
            3: "Ошибка",
            4: "Отправил пакет",
            5: "Отправленный пакет обработан"
        }

        # Запись в файл.
        with open(path, "a", encoding="utf-8") as file:
            file.write("{time} | {fromm} -> ".format(
                           time=current_datetime.strftime('%Y-%m-%d %H:%M:%S'), fromm=self.participants[fromm]) +
                       "{to} | {type_msg} | {text}\n".format(
                           to=self.participants[to], type_msg=messages[type_text], text=text))


if __name__ == "__main__":
    create_directory()

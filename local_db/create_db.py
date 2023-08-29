import sqlite3
from config import l_db_name, table_name, l_pr_db_name


# Процедура создания таблицы.
def create_table(cursor):
    try:
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS {table_name} (
              `id` INTEGER PRIMARY KEY AUTOINCREMENT,
              `imei` BIGINT(20) NOT NULL,
              `terminal_id` INT(6) NOT NULL,
              `rec_id` INT(6) NOT NULL,
              `event_id` INT(6) NOT NULL,
              `time_recv` DATETIME NOT NULL,
              `time_event` INT(8) NOT NULL,
              `lat` DOUBLE NOT NULL,
              `lon` DOUBLE NOT NULL,
              `coords_sign` VARCHAR(3) NOT NULL,
              `speed` DOUBLE NOT NULL,
              `vector` INT(3) NOT NULL,
              `height` INT(5) NOT NULL,
              `is_valid` INT(1) NOT NULL,
              `is_blackbox` INT(1) NOT NULL,
              `point_source` INT(1) NOT NULL,
              `fuel_level_1` INT(6) NOT NULL,
              `fuel_level_2` INT(6) NOT NULL,
              `fuel_level_3` INT(6) NOT NULL,
              `fuel_level_4` INT(6) NOT NULL,
              `sensors` VARCHAR(500) NOT NULL)'''.format(table_name=table_name)

        cursor.execute(create_table_query)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    # Подключение к существующей базе данных или создание новой, если её нет.
    connection = sqlite3.connect('{l_db_name}.db'.format(l_db_name=l_db_name))

    cursor = connection.cursor()

    # Создаем таблицу в бд.
    create_table(cursor)

    cursor.close()
    connection.close()

    # Вторая локальная бд.
    connection = sqlite3.connect('{l_pr_db_name}.db'.format(l_pr_db_name=l_pr_db_name))

    cursor = connection.cursor()

    # Создаем таблицу в бд.
    create_table(cursor)

    cursor.close()
    connection.close()

import mysql.connector
from config import host, port, user, password, db_name, table_name


# Процедура создания таблицы.
def create_table(cursor):
    try:
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS {db_name}. {table_name} (
              `id` INT NOT NULL AUTO_INCREMENT,
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
              `sensors` VARCHAR(500) NOT NULL,
              PRIMARY KEY (`id`))
            ENGINE = InnoDB;
            '''.format(db_name=db_name, table_name=table_name)

        cursor.execute(create_table_query)

    except Exception as e:
        print(e)


# Процедура создания бд.
def create_db(cursor):
    try:
        cursor.execute("CREATE DATABASE {db_name}".format(db_name=db_name))

    except Exception as e:
        print(e)


if __name__ == "__main__":
    # удаленная бд имеет иной формат. больше столбцов. так что ее создание стоит удалить
    # Подключаемся к серверу.
    db_connection = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        ssl_disabled=True
    )

    # Создаем курсор.
    cursor = db_connection.cursor()

    # Создаем бд и таблицу.
    create_db(cursor)
    create_table(cursor)

    # Закрываем курсор и соединение.
    cursor.close()
    db_connection.close()

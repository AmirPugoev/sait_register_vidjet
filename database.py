#database.py
import pyodbc
import config

def get_db_connection():
    connection = pyodbc.connect(
        r'Driver={ODBC Driver 17 for SQL Server};'
        r'Server=' + config.DB_SERVER + ';'  # Имя сервера
        r'Database=' + config.DB_NAME + ';'  # Имя базы данных
        r'Trusted_Connection=yes;'  # Использование доверенного соединения
    )
    return connection

def manage_database(table_name=None, event=None, event_date=None, start_time=None, end_time=None, address=None, ticket_count=None):
    tables = []
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Получение списка таблиц
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
        tables = [row.TABLE_NAME for row in cursor.fetchall()]
        
        if table_name and event and event_date and start_time and end_time and address and ticket_count is not None:
            # Вставка записи в основную таблицу
            insert_event_sql = f"INSERT INTO {table_name} (мероприятие, дата, начало_мероприятия, конец_мероприятия, Адрес, количество_мест) VALUES (?, ?, ?, ?, ?, ?)"
            cursor.execute(insert_event_sql, (event, event_date, start_time, end_time, address, ticket_count))
            
            connection.commit()
            print(f"Event added successfully to {table_name}")
    except pyodbc.Error as e:
        print("Error while connecting to SQL Server:", e)
    finally:
        connection.close()
    
    return tables

def register_user(full_name, email, phone_number, museum, event):
    """
    Регистрирует пользователя, добавляя его данные в таблицу Пользователи.
    
    Параметры:
        full_name (str): Полное имя пользователя.
        email (str): Электронная почта пользователя.
        phone_number (str): Номер телефона пользователя.
        museum (str): Музей.
        event (str): Мероприятие.
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        # SQL-запрос для добавления записи в таблицу Пользователи
        sql = """
        INSERT INTO Пользователи (ФИО, Электронная_почта, Номер_телефона, Музей, Мероприятие)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (full_name, email, phone_number, museum, event))
        connection.commit()  # Сохранение изменений в базе данных
        print("Record inserted successfully into Пользователи table")
    except pyodbc.Error as e:
        # Обработка ошибки подключения к базе данных
        print("Error while connecting to SQL Server:", e)
    finally:
        connection.close()
        print("SQL Server connection is closed")


def get_tables():
    tables = []
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
        tables = [row.TABLE_NAME for row in cursor.fetchall()]
    except pyodbc.Error as e:
        print("Error while connecting to SQL Server:", e)
    finally:
        connection.close()
    return tables

def get_table_data(table_name):
    data = []
    columns = []
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [column[0] for column in cursor.description]
        data = cursor.fetchall()
    except pyodbc.Error as e:
        print("Error while connecting to SQL Server:", e)
    finally:
        connection.close()
    return columns, data


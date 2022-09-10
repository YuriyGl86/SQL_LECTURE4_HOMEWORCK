import psycopg2
from customers import Customers

with psycopg2.connect(database='customers', user='postgres', password='1233212123') as conn:
    cust = Customers()
    # cust.drop_all(conn)

    # 1. Функция, создающая структуру БД (таблицы)
    cust.create_structure(conn)

    # 2. Функция, позволяющая добавить нового клиента
    cust.add_customer(conn, 'Иван', 'Иванов', 'ivanov@mail.ru', '+7-911-123-45-67')
    cust.add_customer(conn, 'Петр', 'Петров', 'petrov@mail.ru', '+7-921-123-45-67')
    cust.add_customer(conn, 'Сидор', 'Сидоров', 'sidorov@mail.ru', '+7-905-123-45-67')
    cust.add_customer(conn, 'Павел', 'Павлов', 'pavel@mail.ru')

    # 3. Функция, позволяющая добавить телефон для существующего клиента
    cust.add_phone(conn, 1, '+7-911-456-78-91')
    cust.add_phone(conn, 2, '+7-911-456-78-92')

    # 4. Функция, позволяющая изменить данные о клиенте
    cust.change_customer(conn, 1, first_name='Сергей')
    cust.change_customer(conn, 1, last_name='Сергеев')
    cust.change_customer(conn, 1, email='sergeev@mail.ru')
    cust.change_customer(conn, 1, phone=(1, 'new_sergeev_phone'))
    cust.change_customer(conn, 2, first_name='Александр', last_name='Александров', email='aleksandrov@mail.ru', phone=(2, 'new_aleksandrov_phone'))

    # 5. Функция, позволяющая удалить телефон для существующего клиента
    cust.del_phone(conn, 1, '+7-911-123-45-67')

    # 6. Функция, позволяющая удалить существующего клиента
    cust.del_customer(conn, 2)

    # 7. Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
    print(cust.find_customer(conn, phone_number='+7-911-456-78-91'))
    print(cust.find_customer(conn, first_name='Сидор'))
    print(cust.find_customer(conn, last_name='Павлов'))
    print(cust.find_customer(conn, email='sidorov@mail.ru'))

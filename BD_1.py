import psycopg2
from pprint import pprint
def creat_table(cur):
    '''
    Функция, создающая структуру БД (таблицы)
    '''
    cur.execute("""
        DROP TABLE phones;
        """)
    cur.execute("""
    DROP TABLE clients;
    """)
    cur.execute('''
    CREATE TABLE IF NOT EXISTS clients(
        client_id SERIAL PRIMARY KEY,
        first_name varchar(100),
        last_name varchar(100),
        email varchar(100)
    );
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS phones(
        phone_id SERIAL PRIMARY KEY,
        phones varchar(100),
        client_id INTEGER NOT NULL REFERENCES clients(client_id)
    );
    ''')


def add_client(cur, first_name, last_name, email, phones=None):
    '''
    Функция, позволяющая добавить нового клиента
    '''
    cur.execute('''
    INSERT INTO clients(first_name, last_name, email) VALUES(%s, %s, %s) RETURNING client_id;
        ''', (first_name, last_name, email))
    id = cur.fetchone()[0]
    if phones != None:
        cur.execute('''
        INSERT INTO phones(phones, client_id) VALUES(%s, %s);
            ''', (phones, id))


def get_id_client(cur, phone):
    '''
    Функция, позволяющая узнать список телефонов данного клиента
    '''
    cur.execute('''SELECT client_id FROM phones WHERE phones=%s;''', (phone,))
    return cur.fetchone()[0]

def add_phone(cur, client_id, phone):
    '''
    Функция, позволяющая добавить телефон для существующего клиента
    '''
    cur.execute('''
    INSERT INTO phones(phones, client_id) VALUES(%s, %s);
    ''', (phone, client_id))


def change_client(cur, client_id, first_name=None, last_name=None, email=None, phones=None):
    '''
    Функция, позволяющая изменить данные о клиенте
    '''
    if first_name != None:
        cur.execute('''
        UPDATE clients SET first_name=%s WHERE client_id=%s;
        ''', (first_name, client_id))
    if last_name != None:
        cur.execute('''
        UPDATE clients SET last_name=%s WHERE client_id=%s;
        ''', (last_name, client_id))
    if email != None:
        cur.execute('''
        UPDATE clients SET email=%s WHERE client_id=%s;
        ''', (email, client_id))
    if phones != None:
        delete_allphone(cur, client_id)
        add_phone(cur, client_id, phones)


def delete_allphone(cur, client_id):
    '''
    Функция, позволяющая удалить все телефоны для существующего клиента
    '''
    cur.execute("""DELETE FROM phones WHERE client_id=%s;""", (client_id,))


def delete_phone(cur, client_id, phone):
    '''
    Функция, позволяющая удалить телефон для существующего клиента
    '''
    cur.execute("""DELETE FROM phones WHERE phones=%s AND client_id=%s;""", (phone, client_id,))


def delete_client(cur, client_id):
    '''
    Функция, позволяющая удалить существующего клиента.
    '''
    delete_allphone(cur, client_id)
    cur.execute("""DELETE FROM clients WHERE client_id=%s;""", (client_id,))


def find_client(cur, first_name=None, last_name=None, email=None, phone=None):
    '''
    Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону
    '''
    if phone != None:
        id = get_id_client(cur, phone)
        cur.execute('''SELECT * FROM clients WHERE client_id=%s;''', (id,))
        print(cur.fetchone())
    elif email != None:
        cur.execute('''SELECT * FROM clients WHERE email=%s;''', (email,))
        print(cur.fetchone())
    elif last_name != None:
        if first_name != None:
            cur.execute('''SELECT * FROM clients WHERE last_name=%s AND first_name=%s;''', (last_name, first_name,))
            print(cur.fetchone())
        else:
            cur.execute('''SELECT * FROM clients WHERE last_name=%s;''', (last_name,))
            print(cur.fetchall())
    elif first_name != None:
        cur.execute('''SELECT * FROM clients WHERE first_name=%s;''', (first_name,))
        print(cur.fetchone())
#
def all_clients(cur):
    '''
    Функция позволяющая вывести содержимое всей таблицы клиентов
    '''
    cur.execute('''SELECT * FROM clients''')
    return cur.fetchall()

def all_phones(cur):
    '''
    Функция позволяющая вывести содержимое всей таблицы телефонов
    '''
    cur.execute('''SELECT * FROM phones''')
    return cur.fetchall()

if __name__ == "__main__":
    with psycopg2.connect(database="DB_HW5", user="postgres", password="") as con:
        with con.cursor() as cur:
            creat_table(cur)
            add_client(cur, 'Иван', 'Иванов', 'mail_1@mail.ru', '555-55-55')
            add_client(cur, 'Петр', 'Иванов', 'mail_2@mail.ru', '444-44-44')
            add_client(cur, 'Иван', 'Петров', 'mail_3@mail.ru', '333-33-33')
            add_client(cur, 'Денис', 'Иванов', 'mail_4@mail.ru', '666-66-66')
            add_client(cur, 'Сергей', 'Иванов', 'mail_5@mail.ru', '000-00-00')
            add_phone(cur, 1, '111-11-11')
            add_phone(cur, 2, '777-77-77')
            add_phone(cur, 3, '888-88-88')
            add_phone(cur, 3, '999-99-99')
            pprint(all_clients(cur))
            print()
            pprint(all_phones(cur))
            print()
            print()
            print()
            change_client(cur, 1, first_name='Денис', last_name='Сидоров', email='super_email@gmail.com', phones='222-22-22')
            pprint(all_clients(cur))
            print()
            pprint(all_phones(cur))
            print()
            print()
            print()
            delete_phone(cur, 3, '999-99-99')
            delete_client(cur, 4)
            pprint(all_clients(cur))
            print()
            pprint(all_phones(cur))
            print()
            print()
            print()
            find_client(cur, first_name='Денис', phone='888-88-88')
            print()
            find_client(cur, last_name='Иванов')
            print()
            find_client(cur, first_name='Петр', last_name='Иванов')
            print()
            find_client(cur, email='mail_5@mail.ru')
            print()
            find_client(cur, phone='888-88-88')

import psycopg2


def delete_tables(connect):
    with connect.cursor() as cur:
        cur.execute("""
        DROP TABLE phone;
        DROP TABLE client;
        """)
        connect.commit()


def create_tables(connect):
    with connect.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
            id_client SERIAL PRIMARY KEY,
            first_name VARCHAR(40) NOT NULL,
            last_name VARCHAR(40) NOT NULL,
            email VARCHAR(40) UNIQUE
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS phone(
            id_phone SERIAL PRIMARY KEY,
            number VARCHAR(10) UNIQUE,
            client INTEGER REFERENCES client(id_client)
        );
        """)

        connect.commit()


def add_client(connect, first_name, last_name, email, phones=None):
    with connect.cursor() as cur:
        cur.execute("""
        INSERT INTO client(first_name, last_name, email) VALUES (%s, %s, %s) RETURNING id_client;
        """, (first_name, last_name, email))
        client_id = cur.fetchone()[0]

        for phone in phones:
            cur.execute("""
            INSERT INTO phone(number, client) VALUES (%s, %s) RETURNING number, client;
            """, (phone, client_id))

        connect.commit()


def add_phone_number(connect, client_id, phone):
    with connect.cursor() as cur:
        cur.execute("""
        INSERT INTO phone(number, client) VALUES (%s, %s) RETURNING number, client;
        """, (phone, client_id))

        connect.commit()


def change_client(connect, client_id, first_name=None, last_name=None, email=None, phone=None):
    if first_name != None:
        with connect.cursor() as cur:
            cur.execute("""
            UPDATE client SET first_name=%s WHERE id_client=%s
            RETURNING id_client;
            """, (first_name, client_id))
            print(cur.fetchall())
    if last_name is not None:
        with connect.cursor() as cur:
            cur.execute("""
            UPDATE client SET last_name=%s WHERE id_client=%s
            RETURNING id_client;
            """, (last_name, client_id))
            print(cur.fetchall())
    if email is not None:
        with connect.cursor() as cur:
            cur.execute("""
            UPDATE client SET email=%s WHERE id_client=%s
            RETURNING id_client;
            """, (email, client_id))
            print(cur.fetchall())
    if phone is not None:
        with connect.cursor() as cur:
            cur.execute("""
            SELECT * FROM client c
            LEFT JOIN phone p ON p.client = c.id_client
            WHERE c.id_client=%s;
            """, (client_id,))
            data = cur.fetchall()
            print(data)
            print('Номера телефона, принадлежащие клиенту:')
            for number in data:
                print(number[-2])
            num_for_change = input('Введите номер, который необходимо заменить: ')
            numbers = []
            for number in data:
                numbers.append(number[-2])
            if num_for_change in numbers:
                cur.execute("""
                UPDATE phone SET number=%s WHERE id_phone=%s;
                """, (phone, number[-3]))
                cur.execute("""
                SELECT number FROM phone
                WHERE client=%s;
                """, (client_id,))
                print('Новые данные: ', cur.fetchall())
            else:
                print('Номер введен неверно')


def delete_phone(connect, client_id):
    with connect.cursor() as cur:
        cur.execute("""
        DELETE FROM phone WHERE client=%s;
        """, (client_id,))

        connect.commit()


def delete_client(connect, client_id):
    with connect.cursor() as cur:
        cur.execute("""
        DELETE FROM phone WHERE client=%s;
        """, (client_id,))
        cur.execute("""
        DELETE FROM client WHERE id_client=%s;
        """, (client_id,))

        connect.commit()


def find_client(connect, first_name=None, last_name=None, email=None, phone=None):
    if first_name is not None:
        with connect.cursor() as cur:
            cur.execute("""
            SELECT * FROM client c
            LEFT JOIN phone p ON p.client = c.id_client
            WHERE c.first_name=%s;
            """, (first_name,))
            print('Client_id = ', cur.fetchall()[0][0])

    elif last_name is not None:
        with connect.cursor() as cur:
            cur.execute("""
            SELECT * FROM client c
            LEFT JOIN phone p ON p.client = c.id_client
            WHERE c.last_name=%s;
            """, (last_name,))
            print('Client_id = ', cur.fetchall()[0][0])

    elif email is not None:
        with connect.cursor() as cur:
            cur.execute("""
            SELECT * FROM client c
            LEFT JOIN phone p ON p.client = c.id_client
            WHERE c.email=%s;
            """, (email,))
            print('Client_id = ', cur.fetchall()[0][0])

    elif phone is not None:
        with connect.cursor() as cur:
            cur.execute("""
            SELECT * FROM client c
            LEFT JOIN phone p ON p.client = c.id_client
            WHERE p.number=%s;
            """, (phone,))
            print('Client_id = ', cur.fetchall()[0][0])


with psycopg2.connect(database="netology_db", user="postgres", password="postgres") as conn:
    # delete_tables(conn)
    create_tables(conn)
    #
    add_client(conn, 'fn1', 'ln1', 'e1', ('ttt11', 'ttt12', 'ttt13'))
    add_client(conn, 'fn2', 'ln2', 'e2', ('ttt21', 'ttt22'))
    add_client(conn, 'fn3', 'ln3', 'e3', ('ttt31', 'ttt32', 'ttt33'))
    add_client(conn, 'fn4', 'ln4', 'e4', ('ttt41', 'ttt42', 'ttt43'))
    add_client(conn, 'fn5', 'ln5', 'e5', ('ttt51', 'ttt52'))
    add_client(conn, 'fn6', 'ln6', 'e6', ('ttt61', 'ttt62', 'ttt63'))
    add_client(conn, 'fn7', 'ln7', 'e7', ('ttt71', 'ttt72', 'ttt73'))
    add_client(conn, 'fn8', 'ln8', 'e8', ('ttt81', 'ttt82'))
    add_client(conn, 'fn9', 'ln9', 'e9', ('ttt91', 'ttt92', 'ttt93'))

    # add_phone_number(conn, 8, '98765')
    # delete_phone(conn,3)
    # delete_client(conn,2)
    # find_client(conn, first_name='fn6')
    # find_client(conn, first_name=None, last_name=None, email='e8')

    # find_client(conn, phone = 'ttt91')
    # change_client(conn, 3, first_name='jane_boo', email='wew@')
    # change_client(conn, 1, phone='ne')

conn.close()

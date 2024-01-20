import pandas

def get_client(conn):
    return pandas.read_sql(
    '''
        SELECT * FROM client
    ''', 
    conn
    )


def del_excursion_client(conn, excursion_client_id):
    cur = conn.cursor()
    cur.execute(
        f'''
            UPDATE excursion
            SET available_numbers = available_numbers + 1
            WHERE excursion_id = (SELECT excursion_id FROM excursion_client WHERE excursion_client_id = {excursion_client_id})
        '''
    )
    cur.execute(
        f'''
            DELETE FROM excursion_client
            WHERE
            excursion_client_id = {excursion_client_id}
        '''
    )
    conn.commit()
def get_excursion_client(conn, client_id):
    return pandas.read_sql('''
        SELECT 
            title AS Название, 
            organizator_name AS Авторы,
            start_date AS Дата_ухода, 
            return_date AS Дата_возврата,
            excursion_client_id
        FROM
        client
        JOIN excursion_client USING(client_id)
        JOIN excursion USING(excursion_id)
        JOIN organizator USING(organizator_id)
        WHERE client_id = :id
        ORDER BY 3
    ''', 
    conn, 
    params={"id": client_id}
    )

def get_new_client(conn, new_client):
    cur = conn.cursor()
    cur.execute(
        '''
            INSERT INTO client (client_name)
            VALUES (:new_client)
        ''',
        {"new_client": new_client}
    )
    conn.commit()
    return cur.lastrowid

def borrow_excursion(conn, excursion_id, client_id):
    cur = conn.cursor()
    cur.executescript(
        f'''
            INSERT INTO excursion_client (excursion_id, client_id, start_date, return_date)
            VALUES ({excursion_id}, {client_id}, DATE("NOW"), NULL);

            UPDATE excursion
            SET available_numbers = available_numbers - 1
            WHERE excursion_id = {excursion_id}
        ''',
    )
    conn.commit()

def set_return_date(conn, excursion_client_id):
    cur = conn.cursor()
    cur.execute(
        f'''
            UPDATE excursion_client
            SET return_date = DATE('NOW')
            WHERE excursion_client_id = {excursion_client_id}
        '''
    )
    cur.execute(
        f'''
            UPDATE excursion
            SET available_numbers = available_numbers + 1
            WHERE excursion_id = (SELECT excursion_id FROM excursion_client WHERE excursion_client_id = {excursion_client_id})
        '''
    )
    conn.commit()
import pandas

def get_organizator_count(conn):
    return pandas.read_sql(
        '''
            WITH cte (organizator_name, organizator_count) AS (
                SELECT
                    organizator_name,
                    COUNT(excursion_id)
                FROM
                    organizator 
                    JOIN excursion USING (organizator_id)
                GROUP BY
                    organizator_name
            )
            SELECT * FROM cte
        ''',
        conn
    )

def get_guide_count(conn):
    return pandas.read_sql(
        '''
            WITH cte (guide_name, guide_count) AS (
                SELECT
                    guide_name,
                    COUNT(excursion_id)
                FROM
                    guide
                    JOIN excursion USING (guide_id)
                GROUP BY
                    guide_name
            )
            SELECT * FROM cte
        ''',
        conn
    )

def get_typeExcursion_count(conn):
    return pandas.read_sql(
        '''
            WITH cte (typeExcursion_name, typeExcursion_count) AS (
                SELECT
                    typeExcursion_name,
                    COUNT(excursion_id)
                FROM
                    typeExcursion
                    JOIN excursion USING (typeExcursion_id)
                GROUP BY
                    typeExcursion_name
            )
            SELECT * FROM cte
        ''',
        conn
    )

def get_all_organizator(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT organizator_name FROM organizator")
    organizator = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return organizator

def get_all_guide(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT guide_name FROM guide")
    guide = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return guide

def get_all_typeExcursion(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT typeExcursion_name FROM typeExcursion")
    typeExcursion = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return typeExcursion


def get_filtered_excursion(conn, selected_organizator, selected_guide, selected_typeExcursion):
    return pandas.read_sql(
        '''
            WITH get_organizator (excursion_id, organizator) AS (
                SELECT
                    excursion_id,
                    GROUP_CONCAT(organizator_name, ", ")
                FROM
                    excursion
                    JOIN organizator USING (organizator_id)
                WHERE
                    organizator_name IN {}
                GROUP BY
                    excursion_id
            ),
            get_excursion AS (
                SELECT
                    title,
                    organizator,
                    guide_name,
                    typeExcursion_name,
                    available_numbers,
                    excursion_id
                FROM
                    get_organizator
                    JOIN excursion USING (excursion_id)
                    JOIN typeExcursion USING (typeExcursion_id)
                    JOIN guide USING (guide_id)
                WHERE
                    typeExcursion_name IN {}
                    AND guide_name IN {}
            )
            SELECT
                *
            FROM get_excursion
        '''.format(
                '({})'.format(', '.join([f'"{elem}"' for elem in selected_organizator])),
                '({})'.format(', '.join([f'"{elem}"' for elem in selected_typeExcursion])),
                '({})'.format(', '.join([f'"{elem}"' for elem in selected_guide]))
            ),
        conn
    )
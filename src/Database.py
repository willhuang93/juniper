from datetime import datetime


def initialize_tables(connection):
    """
    This function initializes the tables for the SQLite3 Database.

    :param connection:  SQLite3 connection object
    :return:  None
    """
    clients_table = '''CREATE TABLE IF NOT EXISTS clients(
        client_id INT PRIMARY KEY,
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        zipcode INT,
        country VARCHAR(255)
    );'''

    orders_table = '''CREATE TABLE IF NOT EXISTS orders(
        order_id INT PRIMARY KEY,
        client_id INT,
        ordered_on TIMESTAMP,
        FOREIGN KEY (client_id) REFERENCES clients (client_id)
    );'''

    cursor = connection.cursor()
    cursor.execute(clients_table)
    cursor.execute(orders_table)


def import_data(data, connection):
    """
    Inserts all data that matches the table schema previously defined into their appropriate tables.

    :param data: A dictionary object that holds the data to be inserted into the database
    :param connection: SQLite3 Connection object
    :return:
    """
    def insert_client_data(records, connection):
        cursor = connection.cursor()

        for record in records:
            data_tuple = (record['client_id'],
                          record['first_name'],
                          record['last_name'],
                          record['zipcode'],
                          record['country'])

            sql = f'INSERT OR IGNORE INTO clients(client_id, first_name, last_name, zipcode, country)' \
                f'VALUES(?, ?, ?, ?, ?)'

            cursor.execute(sql, data_tuple)

    def insert_order_data(records, connection):
        cursor = connection.cursor()

        for record in records:
            data_tuple = (record['order_id'],
                          record['client_id'],
                          datetime.strptime(record['ordered_on'], '%Y-%m-%d'))

            sql = f'INSERT OR IGNORE INTO orders(order_id, client_id, ordered_on)' f'VALUES(?, ?, ?)'

            cursor.execute(sql, data_tuple)

    for table in data['tables']:

        table_name = table['table']

        if table_name == 'clients':
            insert_client_data(table['records'], connection)
        elif table_name == 'orders':
            insert_order_data(table['records'], connection)


def query_data(date, connection):
    """
    The first part lists the number of orders made by each client on or before the given date

    Second part lists the number of orders made by each client after the given date

    :param date: The date of which the SQL Query will use to SELECT data
    :param connection: SQLite3 Connection object
    :return: (The client/order data which is before the parameter date, the client/order data which is after the
             parameter date)
    """
    cursor = connection.cursor()

    sql_on_or_before_date = f'''SELECT count(orders.order_id), clients.first_name, clients.last_name, orders.ordered_on
        FROM orders INNER JOIN clients ON orders.client_id = clients.client_id 
        WHERE DATE(orders.ordered_on) <=  DATE(\'{date}\')
        GROUP BY clients.first_name
        ORDER BY COUNT(orders.order_id) DESC;
    '''

    sql_after_date = f'''SELECT count(orders.order_id), clients.first_name, clients.last_name, orders.ordered_on
        FROM orders INNER JOIN clients ON orders.client_id = clients.client_id 
        WHERE DATE(orders.ordered_on) >  DATE(\'{date}\')
        GROUP BY clients.first_name
        ORDER BY COUNT(orders.order_id) DESC;
    '''

    cursor.execute(sql_on_or_before_date)
    on_or_before_result = cursor.fetchall()

    cursor.execute(sql_after_date)
    after_result = cursor.fetchall()

    return on_or_before_result, after_result

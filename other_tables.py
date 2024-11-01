import pymysql

def create_user_table(host, user, password, database, table_name):

    #connect to mysql
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
        )
    
    cursor = connection.cursor()
    drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
    cursor.execute(drop_table_query)

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        Username VARCHAR(255) PRIMARY KEY,
        Password VARCHAR(255)
    );
    """

    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    connection.close()

def create_layover_table(host, user, password, database, table_name):

    #connect to mysql
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
        )
    
    cursor = connection.cursor()
    drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
    cursor.execute(drop_table_query)

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        LayoverID       INT AUTO_INCREMENT PRIMARY KEY,
        PreviousAirport CHAR(3),
        CurrentAirport  CHAR(3),
        NextAirport     CHAR(3),
        TimeInterval    INT,
        Airline         VARCHAR(255),
        Date            DATE
    );
    """

    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    connection.close()
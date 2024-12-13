import pandas as pd
import pymysql

def csv_to_mysql(csv_file_path, host, user, password, database, table_name):
    # Load and preprocess data
    df = pd.read_csv(csv_file_path)
    df = df.where(pd.notnull(df), None)  # Replace NaNs with None for SQL compatibility

    # Connect to MySQL
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    print("Connected to MySQL")

    cursor = connection.cursor()
    drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
    cursor.execute(drop_table_query)

    # Create the table
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        IATA    CHAR(3) PRIMARY KEY,
        ICAO    CHAR(4),
        Name    VARCHAR(225),
        State   VARCHAR(225)
    );
    """
    cursor.execute(create_table_query)

    # Insert CSV data into the created table
    sql_template = f"""
    INSERT INTO {table_name} (IATA, ICAO, Name, State)
    VALUES (%s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        if row['iata'] is None:
            continue
        values = (
            row['iata'],
            row['icao'],
            row['airport'],
            row['region_name']
        )
        cursor.execute(sql_template, values)

    # Commit the transaction
    connection.commit()
    print("Data successfully inserted into MySQL table.")

    # Close the cursor and connection
    cursor.close()
    connection.close()
    print("MySQL connection is closed.")

if __name__ == "__main__":
    csv_file_path = "airport_codes/iata-icao.csv"
    host = "localhost"
    user = "cfakhimi"
    password = "1r1sh"
    database = "cfakhimi"
    table_name = "airports"


    csv_to_mysql(csv_file_path, host, user, password, database, table_name)
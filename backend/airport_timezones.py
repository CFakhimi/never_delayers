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

    # Create the column
    # alter_table_query = f"""
    # ALTER TABLE {table_name}
    # ADD COLUMN Timezone VARCHAR(225);
    # """
    # cursor.execute(alter_table_query)

    # Insert CSV data into the created table
    sql_template = f"""
    UPDATE {table_name} SET Timezone = %s WHERE IATA = %s
    """

    for _, row in df.iterrows():
        values = (
            row['iana_tz'],
            row['iata_code']
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
    csv_file_path = "airport_codes/timezones.csv"
    host = "localhost"
    user = "cfakhimi"
    password = "1r1sh"
    database = "cfakhimi"
    table_name = "airports"


    csv_to_mysql(csv_file_path, host, user, password, database, table_name)
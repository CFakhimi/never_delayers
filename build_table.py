import pandas as pd 
import pymysql

def csv_to_mysql(csv_file_path, host, user, password, database, table_name):
    df = pd.read_csv(csv_file_path)
    df = df.where(pd.notnull(df), None) # Need to do this bc Nan values cause errors

    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    print("Connected to MySQL")

    cursor = connection.cursor()

    column_types = { # May change these later
        'FlightID': 'INT',
        'Airline': 'VARCHAR(255)',
        'FlightNumber': 'INT',
        'Origin': 'VARCHAR(255)',
        'Destination': 'VARCHAR(255)',
        'ScheduledDeparture': 'VARCHAR(255)',
        'ActualDeparture': 'VARCHAR(255)',
        'ScheduledArrival': 'VARCHAR(255)',
        'ActualArrival': 'VARCHAR(255)',
        'DelayMinutes': 'INT',
        'DelayReason': 'VARCHAR(255)'
    }

    # Create the table
    columns = ", ".join([f"{col} {column_types[col]}" for col in column_types]) # May need to fix
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        {columns}
    );
    """
    cursor.execute(create_table_query)

    # Insert CSV data into the created table
    sql_template = f"""
    INSERT INTO {table_name} (FlightID, Airline, FlightNumber, Origin, Destination, ScheduledDeparture, 
    ActualDeparture, ScheduledArrival, ActualArrival, DelayMinutes, DelayReason)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        values = (
            row['FlightID'],
            row['Airline'],
            row['FlightNumber'],
            row['Origin'],
            row['Destination'],
            row['ScheduledDeparture'],
            row['ActualDeparture'],
            row['ScheduledArrival'],
            row['ActualArrival'],
            row['DelayMinutes'],
            row['DelayReason']
        )
        cursor.execute(sql_template, values)

    # Commit the transaction
    connection.commit()
    print("Data successfully inserted into MySQL table.")

    # Close the cursor and connection
    cursor.close()
    connection.close()
    print("MySQL connection is closed.")

def print_df_info(csv_file_path):
    print(f"Printing info for: {csv_file_path}")
    df = pd.read_csv(csv_file_path)
    for col in df.columns:
        print(f"Column: {col}, Data Type: {df[col].dtype}")

if __name__ == "__main__":
    csv_file_path = "data/flight_delays.csv"
    host = "localhost"
    user = "cfakhimi"
    password = "1r1sh"
    database = "cfakhimi"
    table_name = "flight_delays"

    # Uncomment this to print DataFrame info before inserting to MySQL
    # print_df_info(csv_file_path)

    csv_to_mysql(csv_file_path, host, user, password, database, table_name)

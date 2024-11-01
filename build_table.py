import pandas as pd
import pymysql
import numpy as np

def preprocess_flight_data(df):
    # Selecting and renaming columns to match schema
    df_selected = df[['FL_DATE', 'AIRLINE', 'FL_NUMBER', 'ORIGIN', 'DEST', 'CRS_DEP_TIME', 'DEP_TIME', 
                      'CRS_ARR_TIME', 'ARR_TIME', 'DEP_DELAY', 'DELAY_DUE_CARRIER', 'DELAY_DUE_WEATHER', 
                      'DELAY_DUE_NAS', 'DELAY_DUE_SECURITY', 'DELAY_DUE_LATE_AIRCRAFT']].copy()
    
    # Rename columns to fit schema
    df_selected.rename(columns={
        'AIRLINE': 'Airline',
        'FL_NUMBER': 'FlightNumber',
        'ORIGIN': 'Origin',
        'DEST': 'Destination',
        'DEP_DELAY': 'DelayMinutes',
        'FL_DATE': 'FlightDate'
    }, inplace=True)

    # Separate date and time columns
    df_selected['DepartureDate'] = pd.to_datetime(df_selected['FlightDate']).dt.date
    df_selected['ArrivalDate'] = df_selected['DepartureDate']  # Assuming flights are same-day

    # Ensure time columns are integers and fill missing values
    time_columns = ['CRS_DEP_TIME', 'DEP_TIME', 'CRS_ARR_TIME', 'ARR_TIME']
    for col in time_columns:
        df_selected[col] = df_selected[col].fillna(0).astype(int)

    # Create separate time columns in HH:MM format
    df_selected['ScheduledDepartureTime'] = pd.to_datetime(df_selected['CRS_DEP_TIME'].astype(str).str.zfill(4), format='%H%M', errors='coerce').dt.time
    df_selected['ActualDepartureTime'] = pd.to_datetime(df_selected['DEP_TIME'].astype(str).str.zfill(4), format='%H%M', errors='coerce').dt.time
    df_selected['ScheduledArrivalTime'] = pd.to_datetime(df_selected['CRS_ARR_TIME'].astype(str).str.zfill(4), format='%H%M', errors='coerce').dt.time
    df_selected['ActualArrivalTime'] = pd.to_datetime(df_selected['ARR_TIME'].astype(str).str.zfill(4), format='%H%M', errors='coerce').dt.time

    # Convert NaT values to None for compatibility with SQL
    for col in ['ScheduledDepartureTime', 'ActualDepartureTime', 'ScheduledArrivalTime', 'ActualArrivalTime']:
        df_selected[col] = df_selected[col].where(pd.notnull(df_selected[col]), None).astype(object)

    # Calculate DelayReason based on delay columns
    conditions = [
        (df['DELAY_DUE_CARRIER'] > 0, 'Carrier'),
        (df['DELAY_DUE_WEATHER'] > 0, 'Weather'),
        (df['DELAY_DUE_NAS'] > 0, 'NAS'),
        (df['DELAY_DUE_SECURITY'] > 0, 'Security'),
        (df['DELAY_DUE_LATE_AIRCRAFT'] > 0, 'Late Aircraft')
    ]
    df_selected['DelayReason'] = np.select([cond[0] for cond in conditions], [cond[1] for cond in conditions], default=None)
    
    # Drop original time columns if no longer needed
    df_selected.drop(columns=time_columns + ['FlightDate'], inplace=True)

    return df_selected

def csv_to_mysql(csv_file_path, host, user, password, database, table_name):
    # Load and preprocess data
    df = pd.read_csv(csv_file_path)
    df = preprocess_flight_data(df)
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

    # Define the new schema
    column_types = {
        'FlightID': 'INT',
        'Airline': 'VARCHAR(255)',
        'FlightNumber': 'INT',
        'Origin': 'VARCHAR(255)',
        'Destination': 'VARCHAR(255)',
        'DepartureDate': 'DATE',
        'ArrivalDate': 'DATE',
        'ScheduledDepartureTime': 'TIME',
        'ActualDepartureTime': 'TIME',
        'ScheduledArrivalTime': 'TIME',
        'ActualArrivalTime': 'TIME',
        'DelayMinutes': 'INT',
        'DelayReason': 'VARCHAR(255)'
    }

    # Create the table
    columns = ", ".join([f"{col} {column_types[col]}" for col in column_types if col != 'FlightID'])
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        FlightID INT AUTO_INCREMENT PRIMARY KEY,
        {columns}
    );
    """
    cursor.execute(create_table_query)

    # Insert CSV data into the created table
    sql_template = f"""
    INSERT INTO {table_name} (Airline, FlightNumber, Origin, Destination, DepartureDate, ArrivalDate, 
    ScheduledDepartureTime, ActualDepartureTime, ScheduledArrivalTime, ActualArrivalTime, DelayMinutes, DelayReason)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        values = (
            row['Airline'],
            row['FlightNumber'],
            row['Origin'],
            row['Destination'],
            row['DepartureDate'],
            row['ArrivalDate'],
            row['ScheduledDepartureTime'],
            row['ActualDepartureTime'],
            row['ScheduledArrivalTime'],
            row['ActualArrivalTime'],
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
    csv_file_path = "data/flights_sample_3m.csv"
    host = "localhost"
    user = "cfakhimi"
    password = "1r1sh"
    database = "cfakhimi"
    table_name = "new_flight_delays"

    # Uncomment this to print DataFrame info before inserting to MySQL
    # print_df_info(csv_file_path)

    csv_to_mysql(csv_file_path, host, user, password, database, table_name)

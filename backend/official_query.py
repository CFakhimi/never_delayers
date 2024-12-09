import pymysql
from datetime import datetime

# Globals
HOST = "localhost"
USER = "cfakhimi"
PASSWORD = "1r1sh"
DATABASE = "cfakhimi"

# Decorator to handle database connections
def db_connection(func):
    def with_connection(*args, **kwargs):
        connection = pymysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        cursor = connection.cursor()
        result = func(cursor, *args, **kwargs)
        connection.commit()
        cursor.close()
        connection.close()
        return result

    return with_connection

@db_connection
def insert_flight(cursor, userID, delayMinutes, airline, origin, destination, departureDate, flightNumber=None, scheduledDepartureTime=None, scheduledArrivalTime=None, actualArrivalTime=None):
    # If user does not exist, fail
    if check_user_existence(userID) == False:
        return "User DNE"
    
    table_name = "flight_info"
    query = f"""
    INSERT INTO {table_name} (DelayMinutes, Airline, Origin, Destination, DepartureDate)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (delayMinutes, airline, origin, destination, departureDate,))

    # Eventually figure it out?
    arrivalDate = departureDate
    actualDepartureTime = scheduledDepartureTime
    delayReason = None
    table_name = "flight_creation"
    query = f"""
    INSERT INTO {table_name} (UserID_Fk, FlightID_Fk)
    VALUES (%s, %s)
    """
    flight_id = str(cursor.lastrowid)
    cursor.execute(query, (userID, flight_id))
    return "Success"

@db_connection
def delete_flight(cursor, userID, flightID):
    table_name = "flight_info"
    if verify_user_flight(cursor, userID, flightID) == False:
        return "Unauthorized"
    query = f"DELETE FROM {table_name} WHERE FlightID = %s"
    cursor.execute(query, (flightID,))
    return "Success"

def verify_user_flight(cursor, userID, flightID):
    table_name = "flight_creation"
    id_query = f"""
    SELECT FlightID_Fk
    FROM {table_name}
    WHERE UserID_Fk = %s and FlightID_Fk = %s
    """
    cursor.execute(id_query, (userID,flightID))
    result = cursor.fetchall()
    if result == ():
        return False
    return True

def table_checker(attribute):
    attribute_dict = {
        "FlightID" : "flight_info",
        "Airline" : "flight_info",
        "FlightNumber" : "flight_info",
        "Origin" : "flight_info",
        "Destination" : "flight_info",
        "DelayMinutes" : "flight_info",
        "DelayReason" : "flight_info",
        "DepartureDate" : "flight_info",
        "ArrivalDate" : "flight_times",
        "ScheduledDepartureTime" : "flight_times",
        "ActualDepartureTime" : "flight_times",
        "ScheduledArrivalTime" : "flight_times",
        "ActualArrivalTime" : "flight_times"
    }
    result = attribute_dict.get(attribute, "None")
    return result

@db_connection
def edit_flight(cursor, flightID, attribute, newValue):
    table_name = table_checker(attribute)
    if table_name == "None":
        return "Invalid attribute"
    query = f"UPDATE {table_name} SET {attribute} = %s WHERE FlightID = %s"
    cursor.execute(query, (newValue, flightID))
    return "Updated table"

@db_connection
def get_user_flights(cursor, userID):
    #problably need some sort of userid to flight id check??
    table_name = "flight_creation"
    id_query = f"""
    SELECT FlightID_Fk
    FROM {table_name}
    WHERE UserID_Fk = %s
    """
    cursor.execute(id_query, (userID,))
    flight_ids = cursor.fetchall()
    if flight_ids == ():
        return None
    flight_ids = [str(t[0]) for t in flight_ids]

    # Create a query with placeholders for the IDs
    placeholders = ', '.join(['%s'] * len(flight_ids))
    table_name = "flight_info"
    your_flights_query = f"""
    SELECT FlightID, Airline, Origin, Destination, DepartureDate, DelayMinutes
    FROM {table_name}
    WHERE FlightID IN ({placeholders})
    """

    # Execute the query with the flight IDs as parameters
    cursor.execute(your_flights_query, tuple(flight_ids))
    your_flights = cursor.fetchall()
    flight_keys = ['id', 'airline', 'origin', 'destination', 'departure_date', 'delay_minutes']
    your_flights = [dict(zip(flight_keys, flight)) for flight in your_flights]

    return your_flights
    

@db_connection
def average_delay(cursor, origin, destination, airline, flight_date=None): 
    '''
    cursor, origin, desintation,airline
    '''
    table_name = "flight_info"
    
    if flight_date:
        date = datetime.strptime(flight_date, "%Y-%m-%d")
        month = date.month
        your_delay_query = f"""
        WITH ranked_data AS (
        SELECT 
            DelayMinutes,
            ROW_NUMBER() OVER (ORDER BY DelayMinutes) AS row_num,
            COUNT(*) OVER () AS total_rows
        FROM (SELECT DelayMinutes
            FROM {table_name}
            WHERE Origin = %s AND Destination = %s AND Airline = %s AND month(DepartureDate) = %s) as X)
        SELECT 
            avg(DelayMinutes)
        FROM 
            ranked_data
        WHERE 
            row_num > total_rows * 0.1
            AND row_num <= total_rows * 0.9
        """
    else:
        your_delay_query = f"""
        WITH ranked_data AS (
        SELECT 
            DelayMinutes,
            ROW_NUMBER() OVER (ORDER BY DelayMinutes) AS row_num,
            COUNT(*) OVER () AS total_rows
        FROM (SELECT DelayMinutes
            FROM {table_name}
            WHERE Origin = %s AND Destination = %s AND Airline = %s) as X)
        SELECT 
            avg(DelayMinutes)
        FROM 
            ranked_data
        WHERE 
            row_num > total_rows * 0.1
            AND row_num <= total_rows * 0.9
        """
    cursor.execute(your_delay_query, (origin, destination, airline))
    user_avg_delay = cursor.fetchone()[0]
    
    if user_avg_delay is None:
        #print("No data available for the specified query.")
        return "No delay data available for that flight path."

    return f"Average delay for {airline} from {origin} to {destination}: {user_avg_delay} minutes"

@db_connection
def average_delay_numeric(cursor, origin, destination, airline, flight_date=None): 
    '''
    cursor, origin, desintation,airline
    '''
    table_name = "flight_info"
    
    if flight_date:
        date = datetime.strptime(flight_date, "%Y-%m-%d")
        month = date.month
        your_delay_query = f"""
        WITH ranked_data AS (
        SELECT 
            DelayMinutes,
            ROW_NUMBER() OVER (ORDER BY DelayMinutes) AS row_num,
            COUNT(*) OVER () AS total_rows
        FROM (SELECT DelayMinutes
            FROM {table_name}
            WHERE Origin = %s AND Destination = %s AND Airline = %s AND month(DepartureDate) = %s) as X)
        SELECT 
            avg(DelayMinutes)
        FROM 
            ranked_data
        WHERE 
            row_num > total_rows * 0.1
            AND row_num <= total_rows * 0.9
        """
    else:
        your_delay_query = f"""
        WITH ranked_data AS (
        SELECT 
            DelayMinutes,
            ROW_NUMBER() OVER (ORDER BY DelayMinutes) AS row_num,
            COUNT(*) OVER () AS total_rows
        FROM (SELECT DelayMinutes
            FROM {table_name}
            WHERE Origin = %s AND Destination = %s AND Airline = %s) as X)
        SELECT 
            avg(DelayMinutes)
        FROM 
            ranked_data
        WHERE 
            row_num > total_rows * 0.1
            AND row_num <= total_rows * 0.9
        """
    cursor.execute(your_delay_query, (origin, destination, airline, month))
    user_avg_delay = cursor.fetchone()[0]
    
    return user_avg_delay

@db_connection
def delay_compare(cursor, origin, destination, airline):
    pass

@db_connection
def get_top_flights(cursor, limit=10):
    # This takes a while for some reason
    query = """
    SELECT *
    FROM top_flights
    LIMIT %s
    """
    cursor.execute(query, (limit,))
    return cursor.fetchall()


# Returns True if user exists, false if user does not exist
@db_connection
def check_user_existence(cursor, username):
    table_name = "users"

    username_query = f"""
    SELECT 1
    FROM {table_name}
    WHERE Username = %s
    """
    
    cursor.execute(username_query, (username))
    user = cursor.fetchall()
    if user == ():
        print("User DNE")
        return False
    else:
        print("User exists")
        return True

# Create a new user if they do not already exist
@db_connection
def create_user(cursor, username, password):
    table_name = "users"

    if check_user_existence == True:
        return "Username already taken"

    insert_query = f"""
    INSERT INTO {table_name} (Username, Password)
    VALUES (%s, %s)
    """
    
    cursor.execute(insert_query, (username, password))
    return "Success"

# Check that on attempted login, the username exists and the password is correct
@db_connection
def validate_user(cursor, username, password):
    if check_user_existence(username) == False:
        return "User DNE"
    
    table_name = "users"

    query = f"""
    SELECT Password
    FROM {table_name}
    WHERE Username = %s
    """

    cursor.execute(query, (username))
    stored_password = cursor.fetchone()
    
    if stored_password is not None:
        stored_password = stored_password[0]

    if password == stored_password:
        return "Password is valid"
    else:
        return "Password is invalid"
    
@db_connection
def get_timezone(cursor, code):
    if len(code) == 3:
        code_type = "IATA"
    elif len(code) == 4:
        code_type = "ICAO"
    else:
        return None
    
    table_name = "airports"

    query = f"""
    SELECT Timezone
    FROM {table_name}
    WHERE {code_type} = %s
    """

    cursor.execute(query, (code))
    timezone = cursor.fetchone()

    if timezone is not None:
        timezone = timezone[0]

    return timezone

@db_connection
def airport_to_icao(cursor, code):
    if len(code) != 3:
        return None
    
    table_name = "airports"

    query = f"""
    SELECT ICAO
    FROM {table_name}
    WHERE IATA = %s
    """

    cursor.execute(query, (code))
    icao_code = cursor.fetchone()

    if icao_code is not None:
        icao_code = icao_code[0]

    return icao_code

@db_connection
def airport_to_iata(cursor, code):
    if len(code) != 4:
        return None
    
    table_name = "airports"

    query = f"""
    SELECT IATA
    FROM {table_name}
    WHERE ICAO = %s
    """

    cursor.execute(query, (code))
    iata_code = cursor.fetchone()

    if iata_code is not None:
        iata_code = iata_code[0]

    return iata_code

@db_connection
def airline_to_iata(cursor, code):
    if len(code) != 3:
        return None
    
    table_name = "airlines"

    query = f"""
    SELECT IATA
    FROM {table_name}
    WHERE ICAO = %s
    """

    cursor.execute(query, (code))
    iata_code = cursor.fetchone()

    if iata_code is not None:
        iata_code = iata_code[0]

    return iata_code

@db_connection
def airline_name_to_icao(cursor, airline_name):
    table_name = "airlines"

    query = f"""
    SELECT ICAO
    FROM {table_name}
    WHERE Name = %s
    """

    cursor.execute(query, (airline_name,))
    icao_code = cursor.fetchone()

    if icao_code is not None:
        icao_code = icao_code[0]

    return icao_code



if __name__ == "__main__":
    origin = "JFK"
    destination = "KSFO"
    airline = "United"
    departureDate = "2024-11-03"
    userID = "Alex"
    password = "dAtAbAses"
    delayMinutes = "10"
    #print(average_delay(origin, destination, airline))
    #print(insert_flight(userID, delayMinutes, airline, origin, destination, departureDate))
    delayMinutes= "12"
    #print(insert_flight(userID, delayMinutes, airline, origin, destination, departureDate))
    #print(delete_flight("Fake", "3000008"))
    #print(validate_user(userID, password))
    print(average_delay_numeric('PIT', 'ATL', 'Delta', '2024-10-15'))




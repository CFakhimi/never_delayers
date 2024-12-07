import pymysql

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
   
# Returns a dictionary in the form of {Airline: DelayMinutes}
@db_connection
def all_airline_average_delays(cursor):
    table_name = "flight_info"

    delays_query = f"""
    SELECT Airline, AVG(DelayMinutes)
    FROM {table_name}
    GROUP BY Airline
    """

    cursor.execute(delays_query)
    all_avg_delays = cursor.fetchall()
    delays_dict = {airline: avg_delay for airline, avg_delay in all_avg_delays}
    return dict(all_avg_delays)

@db_connection
def average_delay(cursor, origin, destination, airline, flight_date=None): 
    '''
    cursor, origin, desintation,airline
    '''
    table_name = "flight_info"
    
    your_delay_query = f"""
    SELECT AVG(DelayMinutes)
    FROM {table_name}
    WHERE Origin = %s AND Destination = %s AND Airline = %s
    """
    cursor.execute(your_delay_query, (origin, destination, airline))
    user_avg_delay = cursor.fetchone()[0]
    
    if user_avg_delay is None:
        #print("No data available for the specified query.")
        return "No delay data available for that flight path."

    return f"Average delay for {airline} from {origin} to {destination}: {user_avg_delay} minutes"

@db_connection
def delay_compare(cursor, origin, destination, airline):
    pass

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

if __name__ == "__main__":
    origin = "JFK"
    destination = "SFO"
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
    print(create_user(userID, password))




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
        return "None"
    flight_ids = [str(t[0]) for t in flight_ids]
    ids_string = ', '.join(flight_ids)
    table_name = "flight_info"
    
    #? May need to add more detail to the query
    your_flights_query = f"""
    SELECT Origin, Destination, Airline
    FROM {table_name}
    WHERE FlightID IN %s
    """
    cursor.execute(your_flights_query, (ids_string,))
    your_flights = cursor.fetchall()
    return your_flights
    

@db_connection
def average_delay(cursor, origin, destination, airline): 
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


if __name__ == "__main__":
    origin = "JFK"
    destination = "SFO"
    airline = "United"
    departureDate = "2024-11-03"
    userID = "Jack"
    delayMinutes = "10"
    #print(average_delay(origin, destination, airline))
    #print(insert_flight(userID, delayMinutes, airline, origin, destination, departureDate))
    delayMinutes= "12"
    #print(insert_flight(userID, delayMinutes, airline, origin, destination, departureDate))
    print(delete_flight("Fake", "3000008"))




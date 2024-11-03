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
def insert_flight(cursor, table_name, flightID, airline, flightNumber, origin, destination, departureDate, arrivalDate, scheduledDepartureTime, actualDepartureTime, scheduledArrivalTime, actualArrivalTime, delayMinutes, delayReason):
    query = f"""
    INSERT INTO {table_name} (Airline, FlightNumber, Origin, Destination, DepartureDate, ArrivalDate, 
    ScheduledDepartureTime, ActualDepartureTime, ScheduledArrivalTime, ActualArrivalTime, DelayMinutes, DelayReason)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (flightID, airline, flightNumber, origin, destination, departureDate, arrivalDate, scheduledDepartureTime, actualDepartureTime, scheduledArrivalTime, actualArrivalTime, delayMinutes, delayReason)
    cursor.execute(query, values)

@db_connection
def delete_flight(cursor, table_name, flightID):
    query = f"DELETE FROM {table_name} WHERE FlightID = %s"
    cursor.execute(query, (flightID,))

@db_connection
def edit_flight(cursor, table_name, flightID, attribute, newValue):
    query = f"UPDATE {table_name} SET {attribute} = %s WHERE FlightID = %s"
    cursor.execute(query, (newValue, flightID))

@db_connection
def average_delay(cursor, table_name):
    print("Connected to database")
    
    origin = input("Enter the origin airport initials: ").strip()
    destination = input("Enter the destination airport initials: ").strip()
    airline = input("Enter the airline: ").strip()

    your_delay_query = f"""
    SELECT AVG(DelayMinutes)
    FROM {table_name}
    WHERE Origin = %s AND Destination = %s AND Airline = %s
    """
    cursor.execute(your_delay_query, (origin, destination, airline))
    user_avg_delay = cursor.fetchone()[0]
    
    if user_avg_delay is None:
        print("No data available for the specified query.")
        return -1

    print(f"Average delay for {airline} from {origin} to {destination}: {user_avg_delay} minutes")

    all_airlines_query = f"""
    SELECT Airline, AVG(DelayMinutes) AS avg_delay
    FROM {table_name}
    WHERE Origin = %s AND Destination = %s
    GROUP BY Airline
    ORDER BY avg_delay
    """
    cursor.execute(all_airlines_query, (origin, destination))
    result = cursor.fetchall()

    print("\nAverage delay for all airlines on this route:")
    user_rank = None
    for i, (other_airline, avg_delay) in enumerate(result, 1):
        print(f"{i}. {other_airline}: {avg_delay} minutes")
        if other_airline == airline:
            user_rank = i

    if user_rank:
        print(f"\n{airline} ranks #{user_rank} out of {len(result)} airlines on this route.")

if __name__ == "__main__":
    table_name = "new_flight_delays"
    average_delay(table_name=table_name)

# Need to determine the table_names we need for everything. 
# Need to make sure the user can edit and delete a particular flight
# Need to make it easier for them to insert a flight!!, do this by looking up? Do this maybe be doing math for them??
# Need to fix the date issues maybe???

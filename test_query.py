import pymysql

def insert_flight(host, user, password, database, table_name, flightID, airline, flightNumber, origin, destination, departureDate, arrivalDate, scheduledDepartureTime, actualDepartureTime, scheduledArrivalTime, actualArrival, delayMinutes, delayReason):
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = connection.cursor()

    query = f"""
    INSERT INTO {table_name} (Airline, FlightNumber, Origin, Destination, DepartureDate, ArrivalDate, 
    ScheduledDepartureTime, ActualDepartureTime, ScheduledArrivalTime, ActualArrivalTime, DelayMinutes, DelayReason)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (flightID, airline, flightNumber, origin, destination, departureDate, arrivalDate, scheduledDepartureTime, actualDepartureTime, scheduledArrivalTime, actualArrival, delayMinutes, delayReason)

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

def delete_flight(host, user, password, database, table_name, flightID):
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = connection.cursor()

    query = f"""
    DELETE FROM {table_name} WHERE FlightID = %s
    """

    cursor.execute(query, flightID)
    connection.commit()

    cursor.close()
    connection.close()

def edit_flight(host, user, password, database, table_name, flightID, attribute, newValue):
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = connection.cursor()

    query = f"""
    UPDATE {table_name} SET {attribute} = %s WHERE FlightID = %s
    """

    cursor.execute(query, (newValue, flightID))
    connection.commit()

    cursor.close()
    connection.close()


def average_delay(host, user, password, database, table_name):
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    print("Connected to database")
    
    cursor = connection.cursor()

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

    # Query to get the average delay for all airlines on the same route
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
    for i, (other_airline, avg_delay) in enumerate(result, 1):
        print(f"{i}. {other_airline}: {avg_delay} minutes")
        if other_airline == airline:
            user_rank = i

    print(f"\n{airline} ranks #{user_rank} out of {len(result)} airlines on this route.")

    cursor.close()
    connection.close()

if __name__ == "__main__":
    host = "localhost"
    user = "cfakhimi"
    password = "1r1sh"
    database = "cfakhimi"
    table_name = "new_flight_delays"

    average_delay(host, user, password, database, table_name)

import pymysql

def split_table(host, user, password, database, oldTable, table1, table2):

    #connect to mysql
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
        )
    
    cursor = connection.cursor()

    create_table1_query = f"""
    CREATE TABLE IF NOT EXISTS {table1} (
        FlightID        INT AUTO_INCREMENT PRIMARY KEY,
        Airline         VARCHAR(255),
        FlightNumber    INT,
        Origin          CHAR(3),
        Destination     CHAR(3),
        DelayMinutes    INT,
        DelayReason     VARCHAR(225)
    );
    """
    cursor.execute(create_table1_query)

    create_table2_query = f"""
    CREATE TABLE IF NOT EXISTS {table2} (
        FlightID_FK             INT AUTO_INCREMENT PRIMARY KEY,
        DepartureDate           DATE,
        ArrivalDate             DATE,
        ScheduledDepartureTime  TIME,
        ActualDepartureTime     TIME,
        ScheduledArrivalTime    TIME,
        ActualArrivalTime       TIME,
        FOREIGN KEY(FlightID_FK)
	  		REFERENCES flight_info(FlightID)
			ON DELETE CASCADE
		    ON UPDATE CASCADE
    );
    """
    cursor.execute(create_table2_query)

    fill_table1_query = f"""
    INSERT INTO {table1} (
    FlightID, Airline, FlightNumber, Origin, Destination, DelayMinutes, DelayReason
    )
    SELECT FlightID, Airline, FlightNumber, Origin, Destination, DelayMinutes, DelayReason
    FROM {oldTable};
    """

    cursor.execute(fill_table1_query)

    fill_table2_query = f"""
    INSERT INTO {table2} (
    FlightID_FK, DepartureDate, ArrivalDate, ScheduledDepartureTime, ActualDepartureTime, ScheduledArrivalTime, ActualArrivalTime
    )
    SELECT FlightID, DepartureDate, ArrivalDate, ScheduledDepartureTime, ActualDepartureTime, ScheduledArrivalTime, ActualArrivalTime
    FROM {oldTable};
    """

    cursor.execute(fill_table2_query)


    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    host = "localhost"
    user = "cfakhimi"
    password = "1r1sh"
    database = "cfakhimi"
    oldTable = "new_flight_delays"
    table1 = "flight_info"
    table2 = "flight_times"

    split_table(host, user, password, database, oldTable, table1, table2)
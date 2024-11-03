import pymysql

def create_user_table(host, user, password, database, table_name):

    #connect to mysql
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
        )
    
    cursor = connection.cursor()

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        Username VARCHAR(255) PRIMARY KEY,
        Password VARCHAR(255)
    );
    """

    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    connection.close()

def create_layover_table(host, user, password, database, table_name):

    #connect to mysql
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
        )
    
    cursor = connection.cursor()

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        LayoverID       INT AUTO_INCREMENT PRIMARY KEY,
        PreviousAirport CHAR(3),
        CurrentAirport  CHAR(3),
        NextAirport     CHAR(3),
        TimeInterval    INT,
        Airline         VARCHAR(255),
        Date            DATE,
        UserID_FK       VARCHAR(255),
	    FOREIGN KEY(UserID_FK)
	  		REFERENCES users(Username)
			ON DELETE SET NULL
		    ON UPDATE CASCADE
    );
    """

    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    connection.close()

def create_flight_to_user_table(host, user, password, database, table_name):

    #connect to mysql
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
        )
    
    cursor = connection.cursor()

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        FlightID_FK     INT,
        UserID_FK       VARCHAR(255),
    	FOREIGN KEY(FlightID_FK)
	  		REFERENCES new_flight_delays(FlightID)
			ON DELETE SET NULL
		    ON UPDATE CASCADE,
	    FOREIGN KEY(UserID_FK)
	  		REFERENCES users(Username)
			ON DELETE SET NULL
		    ON UPDATE CASCADE
    );
    """

    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    host = "localhost"
    user = "cfakhimi"
    password = "1r1sh"
    database = "cfakhimi"

    table_name = "users"
    create_user_table(host, user, password, database, table_name)

    table_name = "layovers"
    create_layover_table(host, user, password, database, table_name)

    table_name = "flight_creation"
    create_flight_to_user_table(host, user, password, database, table_name)
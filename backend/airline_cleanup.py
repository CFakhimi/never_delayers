import pymysql

def rename_airlines(host, user, password, database, table_name):

    #connect to mysql
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
        )
    
    cursor = connection.cursor()
    airlines = {
        "United Air Lines Inc."               : "United",
        "Delta Air Lines Inc."                : "Delta",
        "Spirit Air Lines"                    : "Spirit",
        "Southwest Airlines Co."              : "Southwest",
        "American Airlines Inc."              : "American",
        "Republic Airline"                    : "Republic",
        "Alaska Airlines Inc."                : "Alaska Airlines",
        "JetBlue Airways"                     : "Jetblue",
        "PSA Airlines Inc."                   : "PSA Airlines",
        "Allegiant Air"                       : "Allegiant",
        "ExpressJet Airlines LLC d/b/a aha!"  : "ExpressJet",
        "SkyWest Airlines Inc."               : "SkyWest",
        "Endeavor Air Inc."                   : "Endeavor Air",
        "Frontier Airlines Inc."              : "Frontier",
        "Mesa Airlines Inc."                  : "Mesa Airlines",                      
        "Hawaiian Airlines Inc."              : "Hawaiian Airlines"
    }

    for oldName, newName in airlines.items():
        print(f'Renaming {oldName} to {newName}')
        query = f"""
        UPDATE {table_name}
        SET Airline = %s
        WHERE Airline = %s;
        """
        cursor.execute(query, (newName, oldName))
    
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    host = "localhost"
    user = "cfakhimi"
    password = "1r1sh"
    database = "cfakhimi"

    table_name = "new_flight_delays"
    rename_airlines(host, user, password, database, table_name)
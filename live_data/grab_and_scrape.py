from datetime import datetime
import pytz
from flight_grabber import find_matching_planes
from flight_scraper import fetch_flight_times
from backend.official_query import get_timezone, airport_to_icao, airline_to_iata, airline_name_to_icao


def get_timezone_wrapper(airport_code):
    timezone_name = get_timezone(airport_code)
    return pytz.timezone(timezone_name)

def analyze_flights(dep, arr, airline, start_hour, finish_hour, date=None, delta=3):
    if date:
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
        year, month, day = parsed_date.year, parsed_date.month, parsed_date.day
    else:
        now = datetime.now()
        year, month, day = now.year, now.month, now.day

    # Convert start and finish times to hours
    #start_hour = int(start_time.split(":")[0])
    #finish_hour = int(finish_time.split(":")[0])

    # Grab flights using the flight grabber
    flights = find_matching_planes(airport_to_icao(dep), start_hour, get_timezone_wrapper(dep), airport_to_icao(arr), finish_hour, get_timezone_wrapper(arr), date, delta)
    airline_code = airline_name_to_icao(airline)
    # Filter flights by airline code
    if flights == None:
        return None
    matching_flights = [flight.strip() for flight in flights if flight.startswith(airline_code)]
    print(f"Flights matching chosen airline {airline_code}: {matching_flights}")

    # Scrape flight times and calculate delays
    for flight in matching_flights:
        flight_number = flight[len(airline_code):]  # Extract flight number from callsign
        iata = airline_to_iata(airline_code)
        flight_data = fetch_flight_times(iata, flight_number, year, month, day)

        if flight_data:
            dep_sched = flight_data['scheduled_departure']
            dep_act = flight_data['actual_departure']
            arr_sched = flight_data['scheduled_arrival']
            arr_act = flight_data['actual_arrival']
            #print(flight_data)
            dep_delay = calculate_delay(dep_sched, dep_act)
            arr_delay = calculate_delay(arr_sched, arr_act)

            print(f"\nFlight {flight}:")
            print(f"  Departure Delay: {dep_delay} minutes")
            print(f"  Arrival Delay: {arr_delay} minutes")
            return flight, dep_delay, arr_delay

def calculate_delay(scheduled, actual):
    if len(scheduled[5:]) == 4: 
        scheduled_time, scheduled_tz = scheduled[:-4], scheduled[-4:]
    else:  # 3-character time zone
        scheduled_time, scheduled_tz = scheduled[:-3], scheduled[-3:]
    
    if len(actual[5:]) == 4:  
        actual_time, actual_tz = actual[:-4], actual[-4:]
    else: 
        actual_time, actual_tz = actual[:-3], actual[-3:]

    sched_time = datetime.strptime(scheduled_time.strip(), '%H:%M')
    act_time = datetime.strptime(actual_time.strip(), '%H:%M')

    delay = (act_time - sched_time).total_seconds() / 60  # Convert to minutes
    return delay
    
if __name__ == "__main__":
    dep = "SFO"  # Departure airport code
    arr = "JFK"  # Arrival airport code
    #airline_code = "JBU"  # Airline code 
    airline = "Jetblue"
    start_time = "06:00"
    finish_time = "12:00"
    date = "2024-11-24"  # Optional date, needs to be within 3 days
    delay = calculate_delay('08:00CST', '07:47CST')
    print(delay)
    #analyze_flights(dep, arr, airline, start_time, finish_time, date)

from datetime import datetime
import pytz
from flight_grabber import find_matching_planes
from flight_scraper import fetch_flight_times

airport_timezones = {
    'SFO': 'America/Los_Angeles',
    'JFK': 'America/New_York',
    'ORD': 'America/Chicago',
}
icao_to_iata = {
    'JBU': 'B6',  # JetBlue
    'AAL': 'AA',  # American Airlines
    'DAL': 'DL',  # Delta Air Lines
    'UAL': 'UA',  # United Airlines
    'SWA': 'WN',  # Southwest Airlines
}

def get_timezone(airport_code):
    timezone_name = airport_timezones.get(airport_code)
    if not timezone_name:
        return None
    return pytz.timezone(timezone_name)

def analyze_flights(dep, arr, airline_code, start_time, finish_time, date=None):
    if date:
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
        year, month, day = parsed_date.year, parsed_date.month, parsed_date.day
    else:
        now = datetime.now()
        year, month, day = now.year, now.month, now.day

    # Convert start and finish times to hours
    start_hour = int(start_time.split(":")[0])
    finish_hour = int(finish_time.split(":")[0])

    # Grab flights using the flight grabber
    flights = find_matching_planes("K" + dep, start_hour, get_timezone(dep), "K" + arr, finish_hour, get_timezone(arr), date)

    # Filter flights by airline code
    matching_flights = [flight.strip() for flight in flights if flight.startswith(airline_code)]
    print(f"Flights matching chosen airline {airline_code}: {matching_flights}")

    # Scrape flight times and calculate delays
    for flight in matching_flights:
        flight_number = flight[len(airline_code):]  # Extract flight number from callsign
        iata = icao_to_iata[airline_code]
        flight_data = fetch_flight_times(iata, flight_number, year, month, day)

        if flight_data:
            dep_sched = flight_data['scheduled_departure']
            dep_act = flight_data['actual_departure']
            arr_sched = flight_data['scheduled_arrival']
            arr_act = flight_data['actual_arrival']

            dep_delay = calculate_delay(dep_sched, dep_act)
            arr_delay = calculate_delay(arr_sched, arr_act)

            print(f"\nFlight {flight}:")
            print(f"  Departure Delay: {dep_delay} minutes")
            print(f"  Arrival Delay: {arr_delay} minutes")

def calculate_delay(scheduled, actual):
    sched_time = datetime.strptime(scheduled[:-3], '%H:%M')
    act_time = datetime.strptime(actual[:-3], '%H:%M')
    delay = (act_time - sched_time).total_seconds() / 60  # Convert to minutes
    return delay

if __name__ == "__main__":
    dep = "SFO"  # Departure airport code
    arr = "JFK"  # Arrival airport code
    airline_code = "JBU"  # Airline code
    start_time = "06:00"
    finish_time = "12:00"
    date = "2024-11-14"  # Optional date

    analyze_flights(dep, arr, airline_code, start_time, finish_time, date)

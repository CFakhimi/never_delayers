from opensky_api import OpenSkyApi
from datetime import datetime, timedelta, timezone
import pytz

api = OpenSkyApi(username='cfakhimi', password='1r1sh')

# Helper function to convert local time to UTC timestamp with optional date
def local_to_utc(hour_start, timezone, date=None):
    if date:
        specific_date = datetime.strptime(date, "%Y-%m-%d")
        specific_date = timezone.localize(specific_date)  # Attach the timezone to the date
    else:
        specific_date = datetime.now(timezone)
    
    # Set the local time (hour_start) on the specified date
    local_time = specific_date.replace(hour=hour_start, minute=0, second=0, microsecond=0)
    #print(f"Local Time: {local_time}")
    
    utc_time = local_time.astimezone(pytz.utc)
    #print(f"UTC Time: {utc_time}")
    
    start_time = int(utc_time.timestamp())
    end_time = int((utc_time + timedelta(hours=3)).timestamp())  # Assuming a 3-hour interval, may need to adjust
    return start_time, end_time


def get_departures(airport_code, hour_start, timezone, date=None):
    start_time, end_time = local_to_utc(hour_start, timezone, date)
    return api.get_departures_by_airport(airport_code, start_time, end_time)

def get_arrivals(airport_code, hour_start, timezone, date=None):
    # Important that you offset the time start time by a bit because flights land early due to calculations
    start_time, end_time = local_to_utc(hour_start-1, timezone, date)
    return api.get_arrivals_by_airport(airport_code, start_time, end_time)

# Main function to find matching planes
def find_matching_planes(dep_airport, dep_hour, dep_timezone, arr_airport, arr_hour, arr_timezone, date=None):
    departures = get_departures(dep_airport, dep_hour, dep_timezone, date)
    arrivals = get_arrivals(arr_airport, arr_hour, arr_timezone, date)
    #print(departures)
    #print(arrivals)
    if not departures:
        print("Found no departures")
        return
    if not arrivals:
        print("Found no arrivals")
        return

    # Extract ICAO24 codes (unique aircraft IDs)
    dep_flights = {flight.icao24: flight for flight in departures if flight.icao24}
    arr_flights = {flight.icao24: flight for flight in arrivals if flight.icao24}

    # Find matching aircraft
    matching_planes = set(dep_flights.keys()).intersection(arr_flights.keys())
    print(f"Number of matching planes that took off from {dep_airport} and landed at {arr_airport}: {len(matching_planes)}")
    callsigns = []
    if matching_planes:
        print("Matching Flights:")
        for icao24 in matching_planes:
            dep_flight = dep_flights[icao24]
            arr_flight = arr_flights[icao24]
            callsigns.append(dep_flight.callsign)
            print(f"ICAO24: {icao24}")
            print(f"Callsign: {dep_flight.callsign}")
            #print(f"  Arrival callsign: {arr_flight.callsign}")
            print(f"  Estimated Departure Time: {datetime.fromtimestamp(dep_flight.firstSeen, timezone.utc).astimezone(dep_timezone).strftime('%Y-%m-%d %H:%M:%S')} {dep_timezone.zone}")
            print(f"  Estimated Arrival Time: {datetime.fromtimestamp(arr_flight.lastSeen, timezone.utc).astimezone(arr_timezone).strftime('%Y-%m-%d %H:%M:%S')} {arr_timezone.zone}")
            print("-" * 40)
    return callsigns

if __name__ == "__main__":
    departure_airport = "KSFO"          # ICAO code for SFO
    departure_hour = 6                 # local time
    departure_timezone = pytz.timezone('America/Los_Angeles')  # Pacific Time for SFO

    arrival_airport = "KJFK"            # ICAO code for JFK
    arrival_hour = 14                 # local time
    arrival_timezone = pytz.timezone('America/New_York')       # Eastern Time for JFK

    date = "2024-11-14"  # Example date in YYYY-MM-DD format
    # date = None    

    find_matching_planes(departure_airport, departure_hour, departure_timezone, arrival_airport, arrival_hour, arrival_timezone, date)

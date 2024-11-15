from opensky_api import OpenSkyApi
from datetime import datetime, timedelta, timezone
import pytz

# Initialize OpenSky API with optional authentication (replace with your credentials if available)
api = OpenSkyApi(username='cfakhimi', password='1r1sh')

# Helper function to convert local time to UTC timestamp
def local_to_utc(hour_start, timezone):
    # Set the local time (hour_start) on today's date
    now_local = datetime.now(timezone).replace(hour=hour_start, minute=0, second=0, microsecond=0)
    # Convert to UTC
    now_utc = now_local.astimezone(pytz.utc)
    start_time = int(now_utc.timestamp())
    end_time = int((now_utc + timedelta(hours=2)).timestamp())
    return start_time, end_time

# Function to get departures from a specified airport at a specified local time
def get_departures(airport_code, hour_start, timezone):
    start_time, end_time = local_to_utc(hour_start, timezone)
    return api.get_departures_by_airport(airport_code, start_time, end_time)

# Function to get arrivals at a specified airport at a specified local time
def get_arrivals(airport_code, hour_start, timezone):
    start_time, end_time = local_to_utc(hour_start, timezone)
    return api.get_arrivals_by_airport(airport_code, start_time, end_time)

# Main function to find matching planes
def find_matching_planes(dep_airport, dep_hour, dep_timezone, arr_airport, arr_hour, arr_timezone):
    departures = get_departures(dep_airport, dep_hour, dep_timezone)
    arrivals = get_arrivals(arr_airport, arr_hour, arr_timezone)
    
    # Extract ICAO24 codes (unique aircraft IDs)
    dep_flights = {flight.icao24: flight for flight in departures if flight.icao24}
    arr_flights = {flight.icao24: flight for flight in arrivals if flight.icao24}

    # Find matching aircraft
    matching_planes = set(dep_flights.keys()).intersection(arr_flights.keys())
    print(f"Number of matching planes that took off from {dep_airport} and landed at {arr_airport}: {len(matching_planes)}")
    if matching_planes:
        print("Matching Flights:")
        for icao24 in matching_planes:
            dep_flight = dep_flights[icao24]
            arr_flight = arr_flights[icao24]
            print(f"ICAO24: {icao24}")
            print(f"  Departure callsign: {dep_flight.callsign}")
            print(f"  Arrival callsign: {arr_flight.callsign}")
            print(f"  Estimated Departure Time: {datetime.fromtimestamp(dep_flight.firstSeen, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC")
            print(f"  Estimated Arrival Time: {datetime.fromtimestamp(arr_flight.lastSeen, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC")
            print("-" * 40)

if __name__ == "__main__":
    departure_airport = "KSFO"          # ICAO code for SFO
    departure_hour = 5                 # 8 am local time
    departure_timezone = pytz.timezone('America/Los_Angeles')  # Pacific Time for SFO

    arrival_airport = "KJFK"            # ICAO code for JFK
    arrival_hour = 13               # 12 pm local time
    arrival_timezone = pytz.timezone('America/New_York')       # Eastern Time for JFK

    find_matching_planes(departure_airport, departure_hour, departure_timezone, arrival_airport, arrival_hour, arrival_timezone)

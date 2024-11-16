import requests
from bs4 import BeautifulSoup

def fetch_flight_times(airline, flight_number, year, month, day):
    url = f"https://www.flightstats.com/v2/flight-tracker/{airline}/{flight_number}?year={year}&month={month}&date={day}"
    #print(f"Fetching data from: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Request failed with status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    time_elements = soup.find_all('div', class_='text-helper__TextHelper-sc-8bko4a-0')
    
    times = [element.get_text(strip=True) for element in time_elements]
    #print(times)
    scheduled_departure = times[14] if len(times) > 0 else None
    actual_departure = times[16] if len(times) > 1 else None
    scheduled_arrival = times[27] if len(times) > 2 else None
    actual_arrival = times[29] if len(times) > 3 else None

    # Print the results
    print(f"Scheduled Departure: {scheduled_departure}")
    print(f"Actual Departure: {actual_departure}")
    print(f"Scheduled Arrival: {scheduled_arrival}")
    print(f"Actual Arrival: {actual_arrival}")

    return {'scheduled_departure': scheduled_departure,
        'actual_departure': actual_departure,
        'scheduled_arrival': scheduled_arrival,
        'actual_arrival': actual_arrival}

if __name__ == "__main__":
    airline = 'B6'  # JetBlue's airline code
    flight_number = '816'
    year = '2024'
    month = '11'
    day = '14'

    flight_data = fetch_flight_times(airline, flight_number, year, month, day)
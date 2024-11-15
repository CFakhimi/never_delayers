from bs4 import BeautifulSoup
import requests

path = 'https://www.flightstats.com/v2/flight-tracker'

def flight_num_to_delay(airline, number):
    url = path + '/' + airline + '/' + number
    response = requests.get(url)

    if response.status_code == 200:
        content = response.text
    else:
        print("Request failed")
        return None
    
    soup = BeautifulSoup(content, 'html.parser')

    

if __name__ == "__main__":
    airline = "DAL"
    number = "1383"
    flight_num_to_delay(airline, number)
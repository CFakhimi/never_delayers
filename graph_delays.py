import matplotlib.pyplot as plt
from backend.official_query import get_top_flights, average_delay_numeric, insert_flight
from grab_and_scrape import analyze_flights
from datetime import datetime
import time


# Main script
def main():
    limit = 100
    top_flights = get_top_flights(limit=limit)

    # Hard coded values
    now = datetime.now()
    today_date = now.strftime('%Y-%m-%d')
    delta = 2
    scatter_data = []
    notFound = 0
    user = 'admin'

    with open('predictions.txt', 'a') as file:
        file.write(f'{today_date}\n')

    for flight in top_flights:
        time.sleep(20)
        #print(flight)
        airline, origin, destination, departure, arrival = flight
        print(airline, origin, destination, departure, arrival)
        today_delays = analyze_flights(
            dep=origin, arr=destination, airline=airline,
            start_hour=departure, finish_hour=arrival, date=today_date, delta=delta
        )
        avg_delay = average_delay_numeric(origin, destination, airline, today_date) # Need to add refining for month
        # Need to actually make avg delay a number and not a word?
        if today_delays == None:
            print("Did not fly today")
            notFound += 1
            continue
        flight_number, dep_delay, arr_delay = today_delays
        print(flight_number, avg_delay, dep_delay)
        with open('predictions.txt', 'a') as file:
            file.write(f'{airline},{origin},{destination},{departure},{arrival},{flight_number},{avg_delay},{dep_delay},{arr_delay}\n')
        insert_flight(user, dep_delay, airline, origin, destination, today_date)

    print(f'{notFound} of {limit} flights not found today')    
'''
    flight_labels = [data[0] for data in scatter_data]
    avg_delays = [data[1] for data in scatter_data]
    today_delays = [
        data[2] if data[2] != "Not Flown Today" else None for data in scatter_data
    ]

    plt.figure(figsize=(10, 6))
    plt.scatter(flight_labels, avg_delays, label="Average Delay", color="blue")
    plt.scatter(
        flight_labels,
        [td if td is not None else 0 for td in today_delays],
        label="Today's Delay",
        color="red"
    )

    for i, delay in enumerate(today_delays):
        if delay is None:
            plt.text(
                flight_labels[i], 0, "Not Flown Today", fontsize=9, ha='center', color='red'
            )

    plt.xlabel("Flight Number")
    plt.ylabel("Delay (minutes)")
    plt.title("Flight Delay Comparison: Average vs. Today")
    plt.legend()
    plt.grid(True)
    plt.show()
'''

if __name__ == "__main__":
    main()

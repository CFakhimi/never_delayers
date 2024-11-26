import matplotlib.pyplot as plt
from backend.official_query import get_top_flights, average_delay
from grab_and_scrape import analyze_flights


# Main script
def main():
    top_flights = get_top_flights(limit=10)

    # Hard coded values
    today_date = "2024-11-25"
    delta = 3
    scatter_data = []

    for flight in top_flights:
        #print(flight)
        airline, origin, destination, departure, arrival = flight
        print(airline, origin, destination, departure, arrival)
        today_delays = analyze_flights(
            dep=origin, arr=destination, airline=airline,
            start_hour=departure, finish_hour=arrival, date=today_date, delta=delta
        )
        avg_delay = average_delay(origin, airline, today_date) # Need to add refining for month
        # Need to actually make avg delay a number and not a word?
        if today_delays == None:
            print("Did not fly today")
            continue
        flight_number, today_delay = today_delays
        print(flight_number, avg_delay, today_delay)
        scatter_data.append((flight_number, avg_delay, today_delay))

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


if __name__ == "__main__":
    main()

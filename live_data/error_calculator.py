import csv
from backend.official_query import average_delay_numeric, insert_flight
from tqdm import tqdm

def get_errors():
    path = 'live_data/predictions.txt' # had to fix this to move things around!
    tolerance = 10
    delay = 'dep_delay'

    results = dict()

    with open(path, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row['origin'] is None:
                date = row['airline']
                results[date] = dict()
                results[date]['correct'] = 0
                results[date]['total'] = 0
                continue

            results[date]['total'] += 1
            actual = float(row[delay])
            predicted = float(row['avg_delay'])
            if abs(actual - predicted) <= tolerance:
                results[date]['correct'] += 1

    dates = []
    proportions = []
    for date in sorted(results.keys()):
        proportion = results[date]['correct']/results[date]['total'] * 100
        #print(f'{date}: {proportion:.2f}%')
        dates.append(date)
        proportions.append(proportion)

    return dates, proportions


def fix():
    path = 'predictions.txt'
    outpath = 'better_predictions.txt'

    with open(path, mode='r') as infile, open(outpath, mode='w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in tqdm(reader, total=411):
            if row['avg_delay']:
                origin = row['origin']
                destination = row['destination']
                airline = row['airline']
                row['avg_delay'] = average_delay_numeric(origin, destination, airline)

            writer.writerow(row)

def insert():
    path = 'predictions.txt'
    user = 'admin'

    with open(path, 'r') as file:
        reader = csv.DictReader(file)

        for row in tqdm(reader):
            if row['origin'] is None:
                date = row['airline']
                continue
            
            insert_flight(user, row['dep_delay'], row['airline'], row['origin'], row['destination'], date)

if __name__ == "__main__":
    print(get_errors())
            
import pandas as pd

data = pd.read_csv('../data/flights_sample_3m.csv')

# Handle NaN values in ARR_DELAY by replacing them with 0
data['ARR_DELAY'].fillna(0, inplace=True)

data = data.rename(columns={
    'ORIGIN': 'origin',
    'DEST': 'destination',
    'ARR_DELAY': 'arrival_delay'
})

data['FL_DATE'] = pd.to_datetime(data['FL_DATE'])
data['month'] = data['FL_DATE'].dt.month
data['day_of_week'] = data['FL_DATE'].dt.dayofweek
data['dep_hour'] = (data['CRS_DEP_TIME'] // 100).astype(int)  # Extract hour from CRS_DEP_TIME

# 1. Average delay for each route (origin-destination pair)
route_avg_delay = data.groupby(['origin', 'destination'])['arrival_delay'].mean().reset_index()
route_avg_delay.rename(columns={'arrival_delay': 'avg_route_delay'}, inplace=True)
route_avg_delay.to_csv('route_avg_delay.csv', index=False)
print("Route average delays saved as 'route_avg_delay.csv'")

# 2. Average delay for each route by month
route_month_avg_delay = data.groupby(['origin', 'destination', 'month'])['arrival_delay'].mean().reset_index()
route_month_avg_delay.rename(columns={'arrival_delay': 'avg_route_month_delay'}, inplace=True)
route_month_avg_delay.to_csv('route_month_avg_delay.csv', index=False)
print("Route-month average delays saved as 'route_month_avg_delay.csv'")

# 3. Average delay for each route by month and day of the week
route_month_weekday_avg_delay = data.groupby(['origin', 'destination', 'month', 'day_of_week'])['arrival_delay'].mean().reset_index()
route_month_weekday_avg_delay.rename(columns={'arrival_delay': 'avg_route_month_weekday_delay'}, inplace=True)
route_month_weekday_avg_delay.to_csv('route_month_weekday_avg_delay.csv', index=False)
print("Route-month-weekday average delays saved as 'route_month_weekday_avg_delay.csv'")

# 4. Average delay for each route by month, day of the week, and hour of departure
route_month_weekday_hour_avg_delay = data.groupby(['origin', 'destination', 'month', 'day_of_week', 'dep_hour'])['arrival_delay'].mean().reset_index()
route_month_weekday_hour_avg_delay.rename(columns={'arrival_delay': 'avg_route_month_weekday_hour_delay'}, inplace=True)
route_month_weekday_hour_avg_delay.to_csv('route_month_weekday_hour_avg_delay.csv', index=False)
print("Route-month-weekday-hour average delays saved as 'route_month_weekday_hour_avg_delay.csv'")

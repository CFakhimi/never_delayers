import pandas as pd
import pickle
from datetime import datetime

with open('delay_prediction_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('model_features.pkl', 'rb') as features_file:
    feature_columns = pickle.load(features_file)

route_avg_delay = pd.read_csv('route_avg_delay.csv')
route_month_avg_delay = pd.read_csv('route_month_avg_delay.csv')
route_month_weekday_avg_delay = pd.read_csv('route_month_weekday_avg_delay.csv')
route_month_weekday_hour_avg_delay = pd.read_csv('route_month_weekday_hour_avg_delay.csv')

# Function to predict delay using the ML model
def predict_delay_ml_model(origin, destination, airline, date, dep_hour):
    date = pd.to_datetime(date)
    month = date.month
    day_of_week = date.dayofweek
    input_data = pd.DataFrame({
        'origin': [origin],
        'destination': [destination],
        'month': [month],
        'day_of_week': [day_of_week],
        'dep_hour': [dep_hour],
        'airline': [airline]
    })

    input_data = pd.get_dummies(input_data, columns=['origin', 'destination', 'airline'])
    input_data = input_data.reindex(columns=feature_columns, fill_value=0)

    predicted_delay = model.predict(input_data)[0]
    return predicted_delay

def predict_delay_route_avg(origin, destination):
    route_delay = route_avg_delay[
        (route_avg_delay['origin'] == origin) &
        (route_avg_delay['destination'] == destination)
    ]
    if not route_delay.empty:
        return route_delay['avg_route_delay'].values[0]
    else:
        return None

def predict_delay_route_month_avg(origin, destination, month):
    route_month_delay = route_month_avg_delay[
        (route_month_avg_delay['origin'] == origin) &
        (route_month_avg_delay['destination'] == destination) &
        (route_month_avg_delay['month'] == month)
    ]
    if not route_month_delay.empty:
        return route_month_delay['avg_route_month_delay'].values[0]
    else:
        return None

def predict_delay_route_month_weekday_avg(origin, destination, month, day_of_week):
    route_weekday_delay = route_month_weekday_avg_delay[
        (route_month_weekday_avg_delay['origin'] == origin) &
        (route_month_weekday_avg_delay['destination'] == destination) &
        (route_month_weekday_avg_delay['month'] == month) &
        (route_month_weekday_avg_delay['day_of_week'] == day_of_week)
    ]
    if not route_weekday_delay.empty:
        return route_weekday_delay['avg_route_month_weekday_delay'].values[0]
    else:
        return None

def predict_delay_route_month_weekday_hour_avg(origin, destination, month, day_of_week, dep_hour):
    route_hour_delay = route_month_weekday_hour_avg_delay[
        (route_month_weekday_hour_avg_delay['origin'] == origin) &
        (route_month_weekday_hour_avg_delay['destination'] == destination) &
        (route_month_weekday_hour_avg_delay['month'] == month) &
        (route_month_weekday_hour_avg_delay['day_of_week'] == day_of_week) &
        (route_month_weekday_hour_avg_delay['dep_hour'] == dep_hour)
    ]
    if not route_hour_delay.empty:
        return route_hour_delay['avg_route_month_weekday_hour_delay'].values[0]
    else:
        return None

# Function to get predictions from all five methods
def get_all_predictions(origin, destination, airline, date, dep_hour):
    date = pd.to_datetime(date)
    month = date.month
    day_of_week = date.dayofweek
    
    ml_prediction = predict_delay_ml_model(origin, destination, airline, date, dep_hour)
    
    route_avg_prediction = predict_delay_route_avg(origin, destination)
    
    route_month_avg_prediction = predict_delay_route_month_avg(origin, destination, month)

    route_month_weekday_avg_prediction = predict_delay_route_month_weekday_avg(origin, destination, month, day_of_week)

    route_month_weekday_hour_avg_prediction = predict_delay_route_month_weekday_hour_avg(origin, destination, month, day_of_week, dep_hour)

    print(f"Predicted delay (ML Model): {ml_prediction:.2f} minutes")
    if route_avg_prediction is not None:
        print(f"Predicted delay (Route Average): {route_avg_prediction:.2f} minutes")
    else:
        print("Route Average: No data available for this route.")

    if route_month_avg_prediction is not None:
        print(f"Predicted delay (Route-Month Average): {route_month_avg_prediction:.2f} minutes")
    else:
        print("Route-Month Average: No data available for this route and month.")

    if route_month_weekday_avg_prediction is not None:
        print(f"Predicted delay (Route-Month-Weekday Average): {route_month_weekday_avg_prediction:.2f} minutes")
    else:
        print("Route-Month-Weekday Average: No data available for this route, month, and weekday.")

    if route_month_weekday_hour_avg_prediction is not None:
        print(f"Predicted delay (Route-Month-Weekday-Hour Average): {route_month_weekday_hour_avg_prediction:.2f} minutes")
    else:
        print("Route-Month-Weekday-Hour Average: No data available for this route, month, weekday, and hour.")

# Example of calling get_all_predictions
# Replace with actual values for origin, destination, airline, date, and dep_hour
get_all_predictions('STT', 'ATL', 'Delta Air Lines Inc.', '2022-04-22', 21)

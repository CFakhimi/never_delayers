import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import numpy as np
import pickle

data = pd.read_csv('../data/flights_sample_3m.csv')

# Handle NaN values: fill numerical NaNs with 0 and categorical NaNs with 'Unknown'
data.fillna({
    'ARR_DELAY': 0,
    'CRS_DEP_TIME': data['CRS_DEP_TIME'].mean(),
    'AIRLINE': 'Unknown',
    'ORIGIN': 'Unknown',
    'DEST': 'Unknown'
}, inplace=True)

data['FL_DATE'] = pd.to_datetime(data['FL_DATE'])
data['month'] = data['FL_DATE'].dt.month
data['day_of_week'] = data['FL_DATE'].dt.dayofweek
data['dep_hour'] = (data['CRS_DEP_TIME'] // 100).astype(int)  # Extract hour from CRS_DEP_TIME

data = data.rename(columns={
    'ORIGIN': 'origin',
    'DEST': 'destination',
    'ARR_DELAY': 'arrival_delay',
    'AIRLINE': 'airline'
})

features = data[['origin', 'destination', 'month', 'day_of_week', 'dep_hour', 'airline']]
target = data['arrival_delay']
features = pd.get_dummies(features, columns=['origin', 'destination', 'airline'], drop_first=True)

# Function to train the delay prediction model and save it using pickle
def train_and_save_model():
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"Mean Absolute Error of the model: {mae}")

    with open('delay_prediction_model.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)
        print("Model saved as 'delay_prediction_model.pkl'")
    
    with open('model_features.pkl', 'wb') as features_file:
        pickle.dump(features.columns, features_file)
        print("Feature columns saved as 'model_features.pkl'")

# Train the model and save it
train_and_save_model()

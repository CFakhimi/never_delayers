from flask import Flask, render_template, request, session, jsonify
from flask import redirect, url_for # For better redirects
from flask import flash # Quick user messages
from error_calculator import get_errors
from backend.official_query import all_airline_average_delays, average_delay, insert_flight, \
                                    get_user_flights, delete_flight, edit_flight, \
                                    validate_user, create_user, top_route_delays, \
                                    get_airlines
import os
import json

app = Flask(__name__,
            static_folder=os.path.abspath('./static'),
            template_folder=os.path.abspath('./templates'))
app.secret_key = 'secret_key'  # Fix at some point

def query_database(inputs):
    print("This does nothing")
    return "nothing"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/home', methods=['POST', 'GET'])
def home(): # This is the home page!!!
    userID = session.get('username', 'Not logged in')
    user_flights = get_user_flights(userID=userID)
    #print(user_flights)
    result = None
    # Add post request here
    # This will query the database and return it
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        # Handle form submissions based on the form type
        if form_type == 'predict_delay':
            origin = request.form.get('origin')
            destination = request.form.get('destination')
            airline = request.form.get('airline')
            flight_date = None

            result = average_delay(origin, destination, airline, flight_date)
            print(f"Average delay is {result}")
            result = format_delay_info(result)
            #flash(f'Prediction: The average delay for this flight is {result}.')

        elif form_type == 'upload_flight':
            #userID = request.form.get('userID')
            delayMinutes = request.form.get('delayMinutes')
            origin = request.form.get('origin')
            destination = request.form.get('destination')
            departureDate = request.form.get('departureDate')
            airline = request.form.get('airline')
            
            # Call the upload function
            upload_status = insert_flight(userID, delayMinutes, airline, origin, destination, departureDate)
            if upload_status == "Success":
                result = "Added flight successfully!"
            elif upload_status == "User DNE":
                result = "Please log in to add a flight."
            flash(result)
            #flash(f'Upload Status: {upload_status}')
            return redirect(url_for('home'))

        elif form_type == 'delete_flight':
            flight_id = request.form.get('flight_id')
            delete_status = delete_flight(userID, flight_id)
            if delete_status == "Success":
                result = f"Flight ID {flight_id} deleted successfully."
            else:
                result = f"Failed to delete Flight ID {flight_id}."
            flash(result)
            return redirect(url_for('home'))

        elif form_type == 'edit_flight':
            flight_id = request.form.get('flight_id')
            attribute = request.form.get('attribute')
            new_value = request.form.get('new_value')

            edit_status = edit_flight(flight_id, attribute, new_value)
            if edit_status == "Updated table":
                result = f"Flight ID {flight_id} edited successfully."
            else:
                result = f"Failed to edit Flight ID {flight_id}."
            flash(result)
            return redirect(url_for('home'))

    return render_template('home.html', userID=userID, result=result, user_flights=user_flights, airlines=airline_names)

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def authenticate():
    username = request.form['uname']
    password = request.form['pswd']
    
    userStatus = validate_user(username=username, password=password)
    if userStatus == "Password is valid":  
        session['username'] = username
        flash('Login successful!')
        return redirect(url_for('home'))
    else:
        flash('Invalid username or password')
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('home'))

@app.route('/create_account', methods=['GET'])
def create_account():
    return render_template('create_account.html')

@app.route('/create_account', methods=['POST'])
def register():
    username = request.form['uname']
    password = request.form['pswd']
    passwordConfirm = request.form['pswdConfirm']

    # create_user internally checks if user already exists
    if password == passwordConfirm:
        newUserStatus = create_user(username=username, password=password)
        if newUserStatus == "Success":
            flash('Account created successfully. Please log in.')
        else:
            flash('Account not created. Username already exists.')
    else:
        flash('Account not created. Passwords did not match.')
    return redirect(url_for('login'))

@app.route('/data_visualization', methods=['GET'])
def data_page():
    userID = session.get('username', 'Not logged in')
    # The delays are in the format 'Decimal(__delay__)'
    # Extract out just the delay as a float
    delay_data = {key: float(value) for key, value in average_delay_by_airline.items()}
    #print(type(delay_data))
    #print(delay_data)
    airlines = list(delay_data.keys())
    averageAirlineDelays = list(delay_data.values())
    #print(type(json.dumps(airlines)))
    #print(json.dumps(averageAirlineDelays))
    #print(airlines)
    #print(averageAirlineDelays)
    return render_template('data_visualization.html', userID=userID, airlines=airlines, averageAirlineDelays=averageAirlineDelays, top_routes=top_routes, dates=dates, percentages=percentages)

def format_delay_info(data):
    if data is None:
        return """
            <p class="no-delay-text">No delay data available for this flight path.</p>
            <p class="emote">😢</p>
        """

    flight_date_info = f"<p style='font-size:0.8em; font-family:Arial, sans-serif;'><strong>Date:</strong> {data['flight_date']}</p>" if data['flight_date'] else ""

    avg_delay = data['average_delay']
    if avg_delay > 15:
        color = "red"
    elif avg_delay > 5:
        color = "yellow"
    else:
        color = "green"

    text_style = f"color:{color}; text-shadow: 1px 1px 2px black;"

    return f"""
        <p class="result-text"><strong>Airline:</strong> {data['airline']}</p>
        <p class="result-text"><strong>Origin:</strong> {data['origin']}</p>
        <p class="result-text"><strong>Destination:</strong> {data['destination']}</p>
        {flight_date_info}
        <p class="predicted-delay"><strong>Predicted Delay:</strong> <span style="{text_style}">{avg_delay:.2f} min</span></p>
    """



if __name__ == '__main__':
    top_routes = top_route_delays()
    average_delay_by_airline = all_airline_average_delays()
    airline_names = get_airlines()
    dates, percentages = get_errors()
    app.run(host='db8.cse.nd.edu', debug=True, port="5014")

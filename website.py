from flask import Flask, render_template, request, session, jsonify
from flask import redirect, url_for # For better redirects
from flask import flash # Quick user messages
from live_data.error_calculator import get_errors
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

@app.route('/home', methods=['GET'])
def home(): # This is the home page!!!
    userID = session.get('username', 'Not logged in')
    user_flights = get_user_flights(userID=userID)
    result = session.get('result', None)
    
    # Handle pagifaction of forms
    current_edit_page = None
    current_delete_page = None
    editable_flights = None
    deletable_flights = None
    items_per_page = None
    total_pages = None
    if user_flights:
        items_per_page = 5
        total_pages = (len(user_flights) + items_per_page - 1) // items_per_page
        session['total_pages'] = total_pages
        current_edit_page = session.get('curr_edit_page', 1)
        current_delete_page = session.get('curr_delete_page', 1)
        editable_flights = user_flights[(current_edit_page - 1) * items_per_page : (current_edit_page) * items_per_page]
        deletable_flights = user_flights[(current_delete_page - 1) * items_per_page : (current_delete_page) * items_per_page]

    # print("User edit flights: ", len(editable_flights))
    # print("User del flights: ", len(deletable_flights))
    if user_flights:
        print("Num flights: ", len(user_flights))
    print(current_edit_page)
    print(current_delete_page)
    if editable_flights:
        print(len(editable_flights))

    return render_template('home.html', userID=userID, result=result, 
                           editable_flights=editable_flights, curr_edit_page=current_edit_page,
                           deletable_flights=deletable_flights, curr_delete_page=current_delete_page,
                           total_pages=total_pages, airlines=airline_names)


@app.route('/home', methods=['POST'])
def home_form_submission():
    result = None
    form_type = request.form.get('form_type')
    userID = session.get('username', 'Not logged in')
    # Handle form submissions based on the form type
    if form_type == 'predict_delay':
        origin = request.form.get('origin')
        destination = request.form.get('destination')
        airline = request.form.get('airline')
        flight_date = request.form.get('flight_date')

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
        result = format_upload_status(upload_status)
        #flash(result)
        #flash(f'Upload Status: {upload_status}')
        #return redirect(url_for('home'))

    elif form_type == 'delete_flight':
        flight_id = request.form.get('flight_id')
        delete_status = delete_flight(userID, flight_id)
        result = format_delete_status(delete_status, flight_id)
        #flash(result)
        #return redirect(url_for('home'))
        
    elif form_type == 'edit_flight':
        flight_id = request.form.get('flight_id')
        attribute = request.form.get('attribute')
        new_value = request.form.get('new_value')

        edit_status = edit_flight(flight_id, attribute, new_value)
        result = format_edit_status(edit_status, flight_id)
        #return redirect(url_for('home'))

    if result:
        session['result'] = result
    return redirect(url_for('home'))

@app.route('/next_edit_page', methods=['GET'])
def next_edit_page():
    total_pages = session.get('total_pages', default=1)
    session['curr_edit_page'] = session.get('curr_edit_page', 1) + 1
    if session.get('curr_edit_page') > total_pages:
        session['curr_edit_page'] = total_pages
    return redirect(url_for('home'))

@app.route('/previous_edit_page', methods=['GET'])
def previous_edit_page(): 
    session['curr_edit_page'] = session.get('curr_edit_page', 1) - 1
    if session.get('curr_edit_page') <= 0:
        session['curr_edit_page'] = 1
    return redirect(url_for('home'))

@app.route('/select_edit_page', methods=['POST'])
def select_edit_page():
    new_edit_page = int(request.form.get('new_page'))
    total_pages = session.get('total_pages', default=1)
    if (1 <= new_edit_page) and (new_edit_page <= total_pages):
        session['curr_edit_page'] = new_edit_page
    return redirect(url_for('home')) 

@app.route('/next_delete_page', methods=['GET'])
def next_delete_page():
    total_pages = session.get('total_pages', 1)
    session['curr_delete_page'] = session.get('curr_delete_page', 1) + 1
    if session.get('curr_delete_page') > total_pages:
        session['curr_delete_page'] = total_pages
    return redirect(url_for('home'))

@app.route('/previous_delete_page', methods=['GET'])
def previous_delete_page(): 
    session['curr_delete_page'] = session.get('curr_delete_page', 1) - 1
    if session.get('curr_delete_page') <= 0:
        session['curr_delete_page'] = 1
    return redirect(url_for('home'))

@app.route('/select_delete_page', methods=['POST'])
def select_delete_page():
    new_delete_page = int(request.form.get('new_page'))
    total_pages = session.get('total_pages', default=1)
    if (1 <= new_delete_page) and (new_delete_page <= total_pages):
        session['curr_delete_page'] = new_delete_page
    return redirect(url_for('home')) 

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
    session.pop('total_pages', None)
    session.pop('curr_edit_page', None)
    session.pop('curr_delete_page', None)
    session.pop('result', None)
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
    delay_data = {key: float(value) for key, value in average_delay_by_airline.items()}
    airlines = list(delay_data.keys())
    averageAirlineDelays = list(delay_data.values())
    return render_template('data_visualization.html', userID=userID, airlines=airlines, averageAirlineDelays=averageAirlineDelays, top_routes=top_routes, dates=dates, percentages=percentages)

def format_delay_info(data):
    if data is None:
        return """
            <p class="no-delay-text">No delay data available for this flight path.</p>
            <p class="emote">😢</p>
        """

    flight_date_info = f"<p class='result-text'><strong>Date:</strong> {data['flight_date']}</p>" if data['flight_date'] else "<p class='result-text'><strong>Date:</strong> N/A</p>"

    avg_delay = data['average_delay']
    if avg_delay > 10:
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

def format_upload_status(upload_status):
    base_style = """
        font-size:2em; font-weight:bold; color:white; text-shadow: 1px 1px 2px black;
        text-align:center;margin: 0; padding: 0; line-height: 1.2;"""

    if upload_status == "Success":
        return f"""
            <div style="text-align:center;">
                <p class="result-text" style="{base_style} color:green;">
                    Flight added successfully!
                </p>
                <span style="font-size:3em;">✅</span>
            </div>
        """
    else:
        return f"""
            <div style="text-align:center;">
                <p class="result-text" style="{base_style} color:red;">
                    Please log in to add a flight.
                </p>
                <span style="font-size:3em;">🚫</span>
            </div>
        """
    
def format_edit_status(edit_status, flight_id):
    base_style = """font-size:2em; font-weight:bold; color:white; text-shadow: 1px 1px 2px black;
        text-align:center; padding: 0; margin: 0; line-height: 1.2;"""

    if edit_status == "Updated table":
        return f"""
            <div style="text-align:center;">
                <p class="result-text" style="{base_style} color:lime;">
                    Flight ID {flight_id} edited successfully!
                </p>
                <span style="font-size:3em;">✈️✅</span>
            </div>
        """
    else:
        return f"""
            <div style="text-align:center;">
                <p class="result-text" style="{base_style} color:red;">
                    Failed to edit Flight ID {flight_id}.
                </p>
                <span style="font-size:3em;">⚠️</span>
            </div>
        """
def format_delete_status(delete_status, flight_id):
    base_style = """font-size:2em; font-weight:bold; color:white; text-shadow: 1px 1px 2px black;
        text-align:center; padding: 0; margin: 0; line-height: 1.2;"""

    if delete_status == "Success":
        return f"""
            <div style="text-align:center;">
                <p class="result-text" style="{base_style} color:lime;">
                    Flight ID {flight_id} deleted successfully!
                </p>
                <span style="font-size:3em;">🗑️✅</span>
            </div>
        """
    else:
        return f"""
            <div style="text-align:center;">
                <p class="result-text" style="{base_style} color:red;">
                    Failed to delete Flight ID {flight_id}.
                </p>
                <span style="font-size:3em;">⚠️</span>
            </div>
        """
    

if __name__ == '__main__':
    top_routes = top_route_delays()
    average_delay_by_airline = all_airline_average_delays()
    airline_names = get_airlines()
    dates, percentages = get_errors()
    app.run(host='db8.cse.nd.edu', debug=True, port="5013")

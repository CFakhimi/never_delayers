from flask import Flask, render_template, request, session, jsonify
from flask import redirect, url_for # For better redirects
from flask import flash # Quick user messages
from backend.official_query import average_delay, insert_flight, get_user_flights

app = Flask(__name__)
app.secret_key = 'secret_key'  # Fix at some point

def query_database(inputs):
    print("This does nothing")
    return "nothing"

@app.route('/', methods=['POST', 'GET'])
def index(): # This is the home page!!!
    current_user = session.get('username', 'Not logged in')
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
            #flash(f'Prediction: The average delay for this flight is {result}.')

        elif form_type == 'upload_flight':
            # Extract parameters for uploading flight details
            #userID = request.form.get('userID')
            userID = "Jack"
            delayMinutes = request.form.get('delayMinutes')
            origin = request.form.get('origin')
            destination = request.form.get('destination')
            departureDate = request.form.get('departureDate')
            airline = request.form.get('airline')

            # Call the upload function
            upload_status = insert_flight(userID, delayMinutes, airline, origin, destination, departureDate)
            if upload_status == "Success":
                result = "Added flight successfully!"
            #flash(f'Upload Status: {upload_status}')

    return render_template('index.html', current_user=current_user, result=result)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['uname']
    password = request.form['pswd']
    
    if username == 'user' and password == 'password':  
        session['username'] = username
        flash('Login successful!')
        return redirect(url_for('index'))
    else:
        flash('Invalid username or password')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/create_account', methods=['POST'])
def create_account():
    username = request.form['uname']
    password = request.form['pswd']
    flash('Account created successfully. Please log in.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port="9001")

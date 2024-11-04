from flask import Flask, render_template, request, session
from flask import redirect, url_for # For better redirects
from flask import flash # Quick user messages

app = Flask(__name__)
app.secret_key = 'secret_key'  # Fix at some point

def query_database(inputs):
    print("This does nothing")
    return "nothing"

@app.route('/', methods=['POST', 'GET'])
def index(): # This is the home page!!!
    current_user = session.get('username', 'Not logged in')

    # Add post request here
    # This will query the database and return it
    if request.method == 'POST':
        query_input = request.form['query_input']
        result = query_database(query_input)

    return render_template('index.html', current_user=current_user)

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
    app.run(debug=True)

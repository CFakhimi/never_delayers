# never_delayers: Databases Group Project Repository
This is the final version of the website!

To install the required packages into your virtual environment:
pip install -r requirements.txt

To run the website, assuming the cron does not work:
python website.py

### Current important folders:

backend/: Contains all of the python code for SQL queries as well as building the tables in MySQL

live_data/: Contains all of the live data api and scraping functionality for one of our advanced functions

static/: Contains css and images

templates/: Contains all of the website html

### Most important files:

backend/build_table.py: Builds the table from flight_delays dataset

backend/official_query.py: Contains all of the SQL queries that we use regularly on the website

live_data/grab_and_scrape.py: Combines the grabbing from api and scraping from website to report actual delay for a given flight in the past 3 days

templates/home.html: Contains html for the home page which has most of our website functionality

website.py: Contains the mostly Flask code to run the website 


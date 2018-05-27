# Anti-Stress-Tracker
Project for GCT501 course at KAIST

**Dependencies:**
* Flask (http://flask.pocoo.org/docs/1.0/quickstart/), template renderer: (http://jinja.pocoo.org/docs/2.10/)
* python-fitbit (https://github.com/orcasgit/python-fitbit).  
 After installation, update the PYTHONPATH enviroment 
variable. Add the following lines to your .bashrc file (~/python-fitbit/ is your path to the lib):  
`PYTH_FITBIT_LOCATION=~/python-fitbit/   `   
`export PYTHONPATH=$PYTHONPATH:$PYTH_FITBIT_LOCATION`

**Starting the server**

From the root of the project directory run \
`export FLASK_ENV=development` \
`export FLASK_APP=init.py` \
`flask run`

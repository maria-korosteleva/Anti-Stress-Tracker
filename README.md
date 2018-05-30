# Anti-Stress-Tracker
Project for GCT501 course at KAIST. It aims to provide user-friendly 
stress estimations to help people manage their stress. 
It works with Fitbit Web API and need heart rate data to operate. For testing purposes 
authours used Fitbit Charge 2 wristband.  

##Stress estimation
Estimation of the stress level is based on the Baevsky Stress index formula, that 
estimates stress level using heart rate variability.
For reference see http://www.cardiometry.net/issues/no10-may-2017/heart-rate-variability-analysis
originally from book https://www.twirpx.com/file/2327193/ (in Russian)
#### Formula
    sress_score = AMo / (2 * VR * Mo), 
    where
    R-R interval - time delay between consecutive heart beats (assumed to be inverse value of the bpm)
    Mo - mode - most frequent R-R interval value
    AMo - mode amplitude - % of the intervals corresponding to Mode
    VR - variational range - difference  between min and max R-R intervals 

## Running the app
#### Dependencies:
* Flask (http://flask.pocoo.org/docs/1.0/quickstart/), template renderer: (http://jinja.pocoo.org/docs/2.10/)
* python-fitbit (https://github.com/orcasgit/python-fitbit).

#### Starting the server
    export FLASK_ENV=development
    export FLASK_APP=init.py
    flask run
These commands should be run from the root of the project directory. 
Server running in development mode automatically restarts when code changes.
# Anti-Stress-Tracker
Project for GCT501 course at KAIST. It aims to provide user-friendly 
stress estimations to help people manage their stress. 
It works with Fitbit Web API and need heart rate data to operate. For testing purposes 
authours used Fitbit Charge 2 wristband.  

## Running the app
#### Dependencies:
* Flask (http://flask.pocoo.org/docs/1.0/quickstart/), template renderer: (http://jinja.pocoo.org/docs/2.10/)
* python-fitbit (https://github.com/orcasgit/python-fitbit).
* config.ini file should be prepared and put into project directory (see next session).

#### Starting the server
    export FLASK_ENV=development
    export FLASK_APP=init.py
    flask run
These commands should be run from the root of the project directory. 
Server running in development mode automatically restarts when code changes.

## Accessing your Fitbit data
To make the application work with you personal records from your Fitbit, you need
* Have a Fitbit wristband, that can measure heart rate and Fitbit acccount.
* Register an new app on Fitbit web-site
    * Login into your account on fitbit.com
    * Go to https://dev.fitbit.com/apps/new 
    * Register a new app of PERSONAL type, other parameters are not significant
    * You will receive Client ID and Client Secret of the app
* Receive ACCESS_TOKEN, REFRESH_TOKEN
    * From homepage of you app on dev.fitbit.com (with Client ID info) 
    go to OAuth 2.0 tutorial page (link at the end of the page)
    * Choose Authorization Code Flow 
    * You should allow at least heart rate, sleep and workout scopes
    * Perform steps 1, 1A and 2 to get your access token and refresh token
* At the root of the project directory create config.ini text file of the following format and fill the blanks with the data
 you got. Expires at fill with any int number, e.g. 3600.

##### config.ini format
    [Login Parameters]
    c_id = 
    c_secret = 
    u_id = 
    access_token = 
    refresh_token = 
    expires_at =    
    
You are all set, now you can run the server and see you stress level at http://127.0.0.1/5000

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

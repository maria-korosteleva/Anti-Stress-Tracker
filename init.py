from flask import Flask
from flask import render_template
import StressScoreCalc as SS
import datetime as dt

app = Flask(__name__)


@app.route("/")
def stress_score():
    # Login to fitbit
    # get last availible stress score
    score = SS.StressScoreCalc.get_last_score()
    return render_template('stressScore.html', score=score.score, datetime=score.datetime)


@app.route("/today")
def day_stats():
    # Login to fitbit if not logined yet

    # calc todays stats
    start_time = dt.datetime(2018, 1, 25)
    end_time = dt.datetime(2018, 1, 25, 23, 59, 59)
    interval = dt.time(1, 0, 0)
    stats = SS.StressScoreCalc.get_stat_score(start_time, end_time, interval)

    # output the rendered page
    return render_template('stats.html', title='Today\'s statistics', stats=stats)


@app.route("/week")
def week_stats():
    # Login to fitbit if not logined yet
    start_time = dt.datetime(2018, 1, 25)
    end_time = dt.datetime(2018, 1, 25, 23, 59, 59)
    interval = dt.time(1, 0, 0)
    stats = SS.StressScoreCalc.get_stat_score(start_time, end_time, interval)

    # output the rendered page
    return render_template('stats.html', title='Weeks\'s statistics', stats=stats)

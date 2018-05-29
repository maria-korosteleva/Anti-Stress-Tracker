from flask import Flask
from flask import render_template
import StressScoreCalc as SS
import datetime as dt

app = Flask(__name__)


@app.route("/")
def stress_score():
    # get last availible stress score
    score = SS.get_last_score()
    return render_template('stressScore.html', score=score.value, datetime=score.datetime, sleep=score.sleep)


@app.route("/today")
def day_stats():
    # calc todays stats
    today = dt.datetime.now().date()
    interval = dt.timedelta(minutes=30)
    stats = SS.get_stat_score(today, today+dt.timedelta(1), interval)

    # output the rendered page
    return render_template('stats.html', title='Today\'s statistics', stats=stats)


@app.route("/week")
def week_stats():
    # Login to fitbit if not logined yet
    today = dt.datetime.now().date()
    week_start = today-dt.timedelta(7)
    interval = dt.timedelta(hours=3)
    stats = SS.get_stat_score(week_start, today+dt.timedelta(1), interval)

    title = 'Weeks\'s statistics from ' + week_start.strftime("%Y-%b-%d") \
            + ' to ' + today.strftime("%Y-%b-%d")
    # output the rendered page
    return render_template('stats.html', title=title, stats=stats)

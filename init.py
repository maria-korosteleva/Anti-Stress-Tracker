from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route("/")
def stress_score():
    # Login to fitbit
    # get last availible stress score
    return render_template('stressScore.html', score=50, time='2018-01-31')


@app.route("/today")
def day_stats():
    # Login to fitbit if not logined yet
    # calc todays stats
    # output the rendered page
    return render_template('stats.html', title='Today\'s statistics', text='Here goes the stats of Today stress!')


@app.route("/week")
def week_stats():
    # Login to fitbit if not logined yet
    # calc weekly stats: start - finish - sample rate
    # output the rendered page
    return render_template('stats.html', title='Week\'s statistics', text='Here goes the stats of weekly stress!')
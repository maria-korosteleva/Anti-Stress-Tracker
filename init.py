from flask import Flask
from flask import render_template
import StressScoreCalc as SS
import datetime as dt
import fitbit

app = Flask(__name__)
app.static_folder = 'static'


# @app.route("/")
# def stress_score():
#     # get last availible stress score
#     try:
#         score = SS.get_last_score()
#         return render_template('index.html', score=score.value, datetime=score.datetime, sleep=score.sleep)
#
#     except fitbit.exceptions.HTTPTooManyRequests as exc:
#         message = "Retry after " + str(exc.retry_after_sec / 60) + " minutes"
#         return render_template('error.html', error=message)

@app.route("/")
def stress_score():
    try:
        # get last availible stress score
        score = SS.get_last_score()

        # calc todays stats
        today = dt.datetime.now().date()
        min_interval = dt.timedelta(minutes=15)

        today_stats = SS.get_stat_score(today, today + dt.timedelta(1), min_interval)
        today_stats = [{"label": stat.datetime.time().__str__()[:-3], "value": stat.value} for stat in today_stats]

        week_start = today - dt.timedelta(7)
        hour_interval = dt.timedelta(hours=2)

        week_stats = SS.get_stat_score(week_start, today + dt.timedelta(1), hour_interval)
        week_stats_result = []
        for stat in week_stats:
            dict = {}
            if stat.datetime.hour == 2:
                dict_vline = {}
                dict_vline['label'] = stat.datetime.date().__str__()
                dict_vline['vLine'] = '1'
                dict_vline['dashed'] = '1'
                dict_vline['dashLen'] = '1'
                dict_vline['dashGap'] = '1'
                dict_vline['showLabelBorder'] = '0'
                dict_vline['thickness'] = '1'
                week_stats_result.append(dict_vline)

            dict['label'] = stat.datetime.time().__str__()[:-3]
            # dict['label'] = stat.datetime.date().__str__() if stat.datetime.hour == 2 else stat.datetime.time().__str__()[:-3]

            dict['value'] = stat.value

            week_stats_result.append(dict)
        # week_stats = [{"label": stat.datetime.__str__()[:-3], "value": stat.value} for stat in week_stats]

        return render_template('index.html', score=score.value, datetime=score.datetime, sleep=score.sleep,
                               today_stats=today_stats, week_stats=week_stats_result, today=today)

    except fitbit.exceptions.HTTPTooManyRequests as exc:
        message = "Retry after " + str(exc.retry_after_sec / 60) + " minutes"
        return render_template('error.html', error=message)


@app.route("/today")
def day_stats():
    # calc todays stats
    today = dt.datetime.now().date()
    interval = dt.timedelta(minutes=15)
    try:
        stats = SS.get_stat_score(today, today + dt.timedelta(1), interval)
        # output the rendered page

        # print(stats)
        for stat in stats:
            print(stat.value, stat.datetime, stat.sleep)

        return render_template('stats.html', title='Today\'s statistics', stats=stats)
    except fitbit.exceptions.HTTPTooManyRequests as exc:
        message = "Retry after " + str(exc.retry_after_secs / 60) + " minutes"
        return render_template('error.html', error=message)


@app.route("/week")
def week_stats():
    # Login to fitbit if not logined yet
    today = dt.datetime.now().date()
    week_start = today - dt.timedelta(7)
    interval = dt.timedelta(hours=2)
    try:
        stats = SS.get_stat_score(week_start, today + dt.timedelta(1), interval)
        title = 'Weeks\'s statistics from ' + week_start.strftime("%Y-%b-%d") \
                + ' to ' + today.strftime("%Y-%b-%d")
        # output the rendered page
        return render_template('stats.html', title=title, stats=stats)
    except fitbit.exceptions.HTTPTooManyRequests as exc:
        message = "Retry after " + str(exc.retry_after_secs / 60) + " minutes"
        return render_template('error.html', error=message)

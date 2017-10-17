"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    app.logger.debug("request.args: {}".format(request.args))

    km = request.args.get('km', 999, type=float)
    app.logger.debug("controle (km): {}".format(km))

    brev_dist = request.args.get('brev_dist', 1000, type=int)
    app.logger.debug("brevet distance: {}".format(brev_dist))

    start_time = request.args.get('start_time', '2017-01-01T00:00:00-00:00', type=str)
    app.logger.debug("start time: {}".format(start_time))

    try:
        open_time  = acp_times.open_time( km, brev_dist, start_time)
        close_time = acp_times.close_time(km, brev_dist, start_time)
        result = {"open": open_time, "close": close_time}
        return flask.jsonify(result=result)
    except ValueError as e:
        result = {"exception": str(e)}
        return flask.jsonify(result=result)


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")

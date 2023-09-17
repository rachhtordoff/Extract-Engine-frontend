from flask import request, Blueprint, Response, jsonify, current_app, render_template
from skeleton_login_frontend import app, config
import json

general = Blueprint('general', __name__)


@general.route("/health")
def check_status():
    return Response(response=json.dumps({
        "app": current_app.config["APP_NAME"],
        "status": "OK",
        "headers": request.headers.to_list()
    }),  mimetype='application/json', status=200)


@general.route("/showcase")
def showcase_temp():
    return "this is a test route for the plymouth university showcase"

@app.errorhandler(400)
def Internal_server_error(e):
    return render_template('pages/500.html',logo=config.logo), 400

@app.errorhandler(Exception)
def unhandled_exception(e):
   return render_template('pages/503.html'), 503

@app.errorhandler(404)
def page_not_found(e):
   return render_template('pages/404.html',logo=config.logo), 404

@app.errorhandler(500)
def Internal_server_error(e):
   return render_template('pages/500.html',logo=config.logo), 500

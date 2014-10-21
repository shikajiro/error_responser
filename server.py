# coding=utf-8
import os
import pdb
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, json, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask_bootstrap import Bootstrap
import requests
import pdb

# create our little application :)
# export APP_SETTINGS="config.DevelopmentConfig"
print os.environ['APP_SETTINGS']

app = Flask(__name__)
manager = Manager(app)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
Bootstrap(app)
logger = app.logger

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, error_code, status_code=None, payload=None):
        Exception.__init__(self)
        if error_code in {0, 1, 2, 10, 11, 12, 13, 14}:
            self.error_code = error_code
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_json(self):
        error_json = {
              'error':{
                    'code':self.error_code,
                    'message':"this is error message"
              }
        }
        return error_json

@app.route("/")
def index():
    results = AppSetting.query.all()
    app_settings = []
    for result in results:
        item = {
            "app_name"      :result.app_name,
            "status_code"   :result.status_code,
            "error_code"    :result.error_code
        }
        app_settings.append(item)
    return render_template('show_entries.html', app_settings=app_settings)

@app.route("/<app_name>")
def app_name(app_name):
    app_setting = AppSetting.query.filter_by(app_name=app_name).first()
    if app_setting is None:
        app_setting = AppSetting(app_name=app_name, app_url="", status_code=404, error_code=None)
        db.session.add(app_setting)
        db.session.commit()
    item = {
        "app_name"      :app_setting.app_name,
        "app_url"       :app_setting.app_url,
        "status_code"   :app_setting.status_code,
        "error_code"    :app_setting.error_code
    }
    return render_template('edit_app_setting.html', app_setting=item)

@app.route("/<app_name>", methods=['POST'])
def post_app_name(app_name):
    print request.form
    app_setting = AppSetting.query.filter_by(app_name=app_name).first()
    app_setting.app_url     = request.form["app_url"]
    app_setting.status_code = int(request.form["status_code"])
    app_setting.error_code  = int(request.form["error_code"])
    db.session.add(app_setting)
    db.session.commit()
    return "set %s/%s" % (app_setting.status_code, app_setting.error_code)

@app.route('/<app_name>/<path:path>', methods=['GET','POST'])
def catch_all(app_name, path):
    print 'You want %s path: %s' % (app_name, path)
    print '%s' % request.headers
    app_setting = AppSetting.query.filter_by(app_name=app_name).first()
    if app_setting is None:
        app_setting = AppSetting(app_name=app_name, status_code=404)
        db.session.add(app_setting)
        db.session.commit()

    print "set status code %s, error code %s" % (app_setting.status_code, app_setting.error_code)

    if int(app_setting.status_code)/100 == 2:
        # pdb.set_trace()
        url = app_setting.app_url + path
        # print "%s url %s" % (request.method, url)

        headers = {}
        auth = request.headers.get("Authorization")
        if auth:
            headers["Authorization"] = auth
        # print "headers %s" % headers

        res = ""
        if request.method == 'POST':
            # print "data %s" % request.form
            res = requests.post(url, data=request.form, headers=headers)
        elif request.method == 'GET':
            # print "params %s" % request.args
            res = requests.get(url, params=request.args, headers=headers)
        # print res.url
        # pdb.set_trace()
        return res.text
    else:
        if int(app_setting.error_code) < 0:
            abort(app_setting.status_code)
        else:
            raise InvalidUsage(status_code=app_setting.status_code, error_code=app_setting.error_code)

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_json())
    response.status_code = error.status_code
    return response

class AppSetting(db.Model):
  __tablename__ = 'app_settings'

  id = db.Column(db.Integer, primary_key=True)
  app_name = db.Column(db.String())
  app_url = db.Column(db.String())
  status_code = db.Column(db.Integer())
  error_code = db.Column(db.Integer())

  def __init__(self, app_name, app_url, status_code, error_code):
    self.app_name = app_name
    self.app_url = app_url
    self.status_code = status_code
    self.error_code = error_code

  def __repr__(self):
    return 'AppSetting %d %s %s %d' % (self.id, self.app_name, self.app_url, self.status_code, self.error_code)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    # manager.run()
    # app.run(host='0.0.0.0')
    # app.run()

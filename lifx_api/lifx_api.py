import flask
import json
import requests
from flask import request, render_template
import time
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# initialise flask app
app = flask.Flask(__name__)

# configure flask app and database route
app.config["DEBUG"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lifx_api.sqlite3'

# pass flask app to SQLalchemy class
db = SQLAlchemy(app)

# personal access token for lifx cloud stored in python dict
token = "cd40f48e7c86ee9ebb2735ea322469d238a7f74042a8c197d2310195948d8a7f"
headers = {
    "Authorization": "Bearer %s" % token,
}


# table model including:
# a unique id, time, the request data and the function invoked
class Calls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String, nullable=False)
    request = db.Column(db.String(1000), nullable=False)
    function = db.Column(db.String(200), nullable=False)


# resource acting as guide for the api
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


# resource to return JSON of all lifx devices
@app.route('/api/devices/lifx', methods=['GET'])
def get_all():
    # request to get state of all lifx devices
    lifx = requests.get('https://api.lifx.com/v1/lights/all', headers=headers)
    lifx_dict = lifx.text
    add_data(['Get_devices', lifx_dict])
    return lifx_dict


# resource to switch all devices on or off
@app.route('/api/devices/lifx/switch', methods=['GET', 'POST'])
def switch_all():
    # request to toggle state of all lifx devices
    lifx = requests.post('https://api.lifx.com/v1/lights/all/toggle',
                         headers=headers)
    lifx_dict = lifx.text
    add_data(['Switch', lifx_dict])
    return lifx_dict


# resource to change the colour of a light
@app.route('/api/devices/lifx/colour', methods=['GET', 'POST'])
def change_colour_all():
    # check for colour argument in request
    if 'colour' in request.args:
        colour = str(request.args['colour'])
        payload = {
            "color": colour,
            "power": "on"
        }
        lifx = action(payload)
        lifx_dict = lifx.text
        add_data(['change_colour ' + colour, lifx_dict])
        return lifx_dict
    else:
        return 'please add a colour to the request'


# resource to change the colour of a light for a given time
@app.route('/api/devices/lifx/colourTime', methods=['GET', 'POST'])
def change_colour_timer():
    # check for colour argument in request
    if 'colour' and 'time' in request.args:
        colour = str(request.args['colour'])
        seconds = int(request.args['time'])
        payload = {
            "color": colour,
            "power": "on"
        }
        lifx = action(payload)
        lifx_dict = lifx.text
        add_data(['change_colour_timer ' + colour, lifx_dict])
        time.sleep(seconds)
        payload2 = {
            "color": "white",
            "power": "off"
        }
        lifx = action(payload2)
        return lifx_dict
    else:
        return 'please add a colour and a time to the request'


# resource to turn lights on for a given amount of time
@app.route('/api/devices/lifx/timer', methods=['GET', 'POST'])
def api_timer():
    # check for time argument in request
    if 'time' in request.args:
        seconds = (request.args['time'])
        payload = {
            'power': 'on',
            'color': 'white'
        }
        action(payload)
        time.sleep(int(seconds))
        payload = {
            'power': 'off',
            'color': 'white'
        }
        lifx = action(payload)
        lifx_dict = lifx.text
        add_data(['Timer', lifx_dict])
        return lifx_dict
    else:
        return 'please add a time to the request'


# function to send payloads as a put request to lifx cloud
def action(payload):
    return requests.put('https://api.lifx.com/v1/lights/d073d562fa17/state',
                        data=json.dumps(payload), headers=headers)


# function to add data to the database for each request to the api
def add_data(response_list):
    time = str(datetime.now())
    function = response_list[0]
    response = response_list[1]
    add_data = Calls(time=time, request=response, function=function)
    db.session.add(add_data)
    db.session.commit()


# run the flask app on default port 5000
app.run()

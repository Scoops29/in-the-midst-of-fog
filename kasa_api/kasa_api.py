import kasa
import asyncio
import flask
from flask import request, render_template
import time
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# initialise flask app
app = flask.Flask(__name__)

# configure flask app and database route
app.config["DEBUG"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kasa_api.sqlite3'

# pass flask app to SQLalchemy class
db = SQLAlchemy(app)


# table model including:
# a unique id, time, the request data and the function invoked
class Calls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String, nullable=False)
    request = db.Column(db.String(1000), nullable=False)
    function = db.Column(db.String(200), nullable=False)

# plug ip
ip = "192.168.1.22"


# home page for video demo
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


# resource to receive the state of all kasa devices
@app.route('/api/devices/kasa', methods=['GET'])
def api_all():
    # connect to the plug
    plug = kasa.SmartPlug(ip)
    # update the state of the plug and check whether it is on
    asyncio.run(plug.update())
    state = plug.is_on
    # if on return on
    if state is True:
        kasa_dict = plug.state_information
        kasa_dict["power"] = "on"
        add_data(['Get_devices', str(kasa_dict)])
        return kasa_dict
    # if off return off
    elif state is False:
        kasa_dict = plug.state_information
        kasa_dict["power"] = "off"
        add_data(['Get_devices', str(kasa_dict)])
        return kasa_dict


# resource to switch plug on or off
@app.route('/api/devices/kasa/switch', methods=['GET', 'POST'])
def switch_all():
    # connect to the plug
    plug = kasa.SmartPlug(ip)
    # update the state of the plug and check whether it is on
    asyncio.run(plug.update())
    state = plug.is_on
    # if on turn off and return off
    if state is True:
        asyncio.run(plug.turn_off())
        kasa_dict = plug.state_information
        kasa_dict["power"] = "off"
        add_data(['Switch_off', str(kasa_dict)])
        return kasa_dict
    # else turn on and return on
    else:
        asyncio.run(plug.turn_on())
        kasa_dict = plug.state_information
        kasa_dict["power"] = "on"
        add_data(['Switch_on', str(kasa_dict)])
        return kasa_dict


# resource to put light on a timer
@app.route('/api/devices/kasa/timer', methods=['GET', 'POST'])
def api_timer():
    # connect to the plug
    plug = kasa.SmartPlug(ip)
    # update the state of the plug and check whether it is on
    asyncio.run(plug.update())
    state = plug.is_on
    # check for time argument in request
    if 'time' in request.args:
        seconds = request.args['time']
        # if plug is on keep it on for the given time then turn off
    if state is True:
        time.sleep(int(seconds))
        asyncio.run(plug.turn_off())
        kasa_dict = plug.state_information
        kasa_dict["power"] = "off"
        add_data(['Timer', str(kasa_dict)])
        return kasa_dict
        # if plug is off turn it on for the given time then turn off
    else:
        asyncio.run(plug.turn_on())
        time.sleep(int(seconds))
        asyncio.run(plug.turn_off())
        kasa_dict = plug.state_information
        kasa_dict["power"] = "off"
        add_data(['Timer', str(kasa_dict)])
        return kasa_dict


# function to add data to the database for each request to the api
def add_data(response_list):
    time = str(datetime.now())
    function = response_list[0]
    response = response_list[1]
    add_data = Calls(time=time, request=response, function=function)
    db.session.add(add_data)
    db.session.commit()

# run the flask app on port 80
app.run(port=80)

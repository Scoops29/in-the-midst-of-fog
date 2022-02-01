from gevent import monkey as curious_george
# monkey patch due to potential Python recursion error in grequests
curious_george.patch_all(thread=False, select=False)
from flask import Flask, request, render_template
import requests
import grequests
from datetime import datetime
import time
from flask_sqlalchemy import SQLAlchemy


# initialise flask app and activate debug
app = Flask(__name__)

# configure flask app and database route
app.config["DEBUG"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///netatmo.sqlite3'

# pass flask app to SQLalchemy class
db = SQLAlchemy(app)

# crednetials required to recieve access token to netatmo api
client_id = "6107d7cdf27dbb6a4c0da357"
client_secret = "2oyaDlMB2JLUna9pGSFiQgIJS137dt"
username = "joshwilliamcooper@gmail.com"
password = "Gold-2911"

# scope required with api calls
scope = 'read_camera'

# redirect url to this app home page after user logs in
redirect_url = 'http://127.0.0.1:443'

# url needed to establish webhook endpoint - this changes with each new ngrok tunnel
webhook_url = 'http://e93eab444f22.ngrok.io'


# table model including a unique id, time, the request data and the event
class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String, nullable=False)
    request = db.Column(db.String(1000), nullable=False)
    event = db.Column(db.String(200), nullable=False)


# home page for video demo
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


# resource to login to netatmo account and authorize IoT in the Midst of Fog app to access devices
@app.route('/login', methods=['GET'])
def login():
    request_url = requests.post('https://api.netatmo.com/oauth2/authorize?client_id=' + client_id + '&redirect_uri=' + redirect_url + '/netatmoOAuth&scope=' + scope + '&state=fourtet')
    return 'go to this url and grant access to device: ' + request_url.url


# resource to generate an access token and start a webhook
@app.route('/setup', methods=['GET', 'POST'])
def get_access():
    # credentials needed for access token in python dictionary
    data = dict(grant_type='password', client_id=client_id,
                client_secret=client_secret, username=username,
                password=password, scope=scope)

# request to generate an access token
    resp = requests.post('https://api.netatmo.com/oauth2/token', data=data)
    if resp.status_code == 200:
        token = resp.json()
        token['expiry'] = int(time.time()) + token['expires_in']
        access_token = token['access_token']
        refresh_token = token['refresh_token']
# request to add a webhook to netatmo account
    add_webhook_url = "https://api.netatmo.com/api/addwebhook?url=" + webhook_url + "/webhook"
    response = requests.get(add_webhook_url, headers={'authorization': 'Bearer ' + access_token})
    return("access: " + access_token + " refresh : " + refresh_token + "webhook_status:" + response.text)


# resource to listen to webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # print the request and send it to be handled by the action manage function
    netatmo_dict = request.json
    if netatmo_dict['event_type'] == 'movement':
        print(netatmo_dict['message'])
    elif netatmo_dict['event_type'] == 'person':
        print(netatmo_dict['snapshot_url'])
    action_manage(request)
    return 'events are handled in action_manage function'


# function to handle data received from the webhook and to make request to other APIs based on this data
def action_manage(response):
    netatmo_dict = response.json
    # when camera detects movement turn lights on for 10 seconds
    if netatmo_dict['event_type'] == 'movement':
        urls = [
               'http://127.0.0.1:5000/api/devices/lifx/timer?time=10',
               'http://127.0.0.1:80//api/devices/kasa/timer?time=10'
        ]
        requests = (grequests.get(u) for u in urls)
        response = grequests.map(requests)
        add_data([netatmo_dict['event_type'], response[0].text, response[1].text])
    # when camera doesn't recognise a face turn light red
    elif netatmo_dict['persons'][0]['is_known'] is False:
        urls = [
               'http://127.0.0.1:5000/api/devices/lifx/colourTime?time=10&colour=red',
               'http://127.0.0.1:80//api/devices/kasa/timer?time=10'
        ]
        requests = (grequests.get(u) for u in urls)
        response = grequests.map(requests)
        add_data([netatmo_dict['event_type'], response[0].text, response[1].text])
    # when camera recognises a face turn light green
    elif netatmo_dict['persons'][0]['is_known'] is True:
        urls = [
                'http://127.0.0.1:5000/api/devices/lifx/colourTime?time=10&colour=green',
                'http://127.0.0.1:80//api/devices/kasa/timer?time=10'
        ]
        requests = (grequests.get(u) for u in urls)
        response = grequests.map(requests)
        add_data([netatmo_dict['event_type'],
                 response[0].text, response[1].text])
    else:
        return netatmo_dict


# function to add data to the database for each request to the api
def add_data(response_list):
    time = str(datetime.now())
    event = response_list[0]
    response = response_list[1] + response_list[2]
    add_event = Events(time=time, request=response, event=event)
    db.session.add(add_event)
    db.session.commit()

# run app on port 443
app.run(port=443)

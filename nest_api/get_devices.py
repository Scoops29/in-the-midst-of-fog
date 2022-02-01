import requests 
import nest_codes 


url_get_devices = 'https://smartdevicemanagement.googleapis.com/v1/enterprises/' + nest_codes.project_id + '/devices'

headers = {
    'Content-Type': 'application/json',
    'Authorization': nest_codes.access_token,
    }

response = requests.get(url_get_devices, headers=headers)

response_json = response.json()
device_name = response_json['devices'][0]['name']
print(device_name)
import requests 
import nest_codes
import get_devices

url_get_device = 'https://smartdevicemanagement.googleapis.com/v1/' + get_devices.device_name


headers = {
    'Content-Type': 'application/json',
    'Authorization': nest_codes.access_token,
}

response = requests.get(url_get_device, headers=headers)

response_json = response.json()
print(response.text)



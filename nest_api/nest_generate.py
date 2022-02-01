project_id = 'a62c6996-a02f-47d7-ae7f-3b4b9fd7de8e'
client_id = '313671465709-1i8b8mi5ug8969k7jq1macmdorddkc8n.apps.googleusercontent.com'
client_secret = 'pMuqQAd_BaJgpMHyedmII06h'
redirect_uri = 'https://www.google.com'

url = 'https://nestservices.google.com/partnerconnections/'+project_id+'/auth?redirect_uri='+redirect_uri+'&access_type=offline&prompt=consent&client_id='+client_id+'&response_type=code&scope=https://www.googleapis.com/auth/sdm.service'
#print("Go to this URL to log in:")
#print(url)

code = '4/0AX4XfWgeMZLXuPFneTwjDdzq_FIrSwIUPtdRtjMK2H-VVxx_KSed8abujsnOWaSu7ocN_g&scope=https://www.googleapis.com/auth/sdm.service'
code1 = '?code=4/0AX4XfWgeMZLXuPFneTwjDdzq_FIrSwIUPtdRtjMK2H-VVxx_KSed8abujsnOWaSu7ocN_g&scope=https://www.googleapis.com/auth/sdm.service'

access_token = 'Bearer ya29.a0ARrdaM-dSIP6fLIPSI-KaXNN5xnocyvDmeKdZiuU83j0mspfsnLvmv6eUOwO9pl2gLQ2r89Zal837hP483j4F4-fHSVECvhtjMZa1kRMvQWQK6lFnYRF59KPD6JJBs4z_Tj4pK1sWVa5KhgIbRsZLFpUn3UJ'
refresh_token = '1//03jlOJQ_GNNFjCgYIARAAGAMSNwF-L9IrOZSM0Lr4yiwnX8YSle1B0c3n2oE0fAEUZYneJk807hF96YydmwwE_3YfXVbWyg5RAUw'

import requests 

def get_token():
    params = (
        ('client_id', client_id),
        ('client_secret', client_secret),
        ('code', code),
        ('grant_type', 'authorization_code'),
        ('redirect_uri', redirect_uri),
)

    response = requests.post('https://www.googleapis.com/oauth2/v4/token', params=params)

    response_json = response.json()
    access_token = response_json['token_type'] + ' ' + str(response_json['access_token'])
    print('Access token: ' + access_token)
    refresh_token = response_json['refresh_token']
    print('Refresh token: ' + refresh_token)

def refresh():
    params = (
        ('client_id', client_id),
        ('client_secret', client_secret),
        ('refresh_token', refresh_token),
        ('grant_type', 'refresh_token'),
)
    response = requests.post('https://www.googleapis.com/oauth2/v4/token', params=params)

    response_json = response.json()
    access_token = response_json['token_type'] + ' ' + response_json['access_token']
    print('Access token: ' + access_token)
    
    
url_get_devices = 'https://smartdevicemanagement.googleapis.com/v1/enterprises/' + project_id + '/devices'

headers = {
    'Content-Type': 'application/json',
    'Authorization': access_token,
    }

response = requests.get(url_get_devices, headers=headers)

print(response.json())
response_json = response.json()
device_0_name = response_json['devices'][0]['name']
print(device_0_name)
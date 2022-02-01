# various ids are required to generate authyentification this code holds these variables 
# id of the in the midst of fog project on google console.nest
project_id = 'a62c6996-a02f-47d7-ae7f-3b4b9fd7de8e'
# if of the auth2 client hosted in the google cloud platform 
client_id = '313671465709-1i8b8mi5ug8969k7jq1macmdorddkc8n.apps.googleusercontent.com'
# secret code to generate new id from the google cloud platform 
client_secret = 'pMuqQAd_BaJgpMHyedmII06h'
# redirect url to app homepage (temporary)
redirect_uri = 'https://www.google.com'

# url to login to allow google account and linked devices access to this app 
url = 'https://nestservices.google.com/partnerconnections/'+project_id+'/auth?redirect_uri='+redirect_uri+'&access_type=offline&prompt=consent&client_id='+client_id+'&response_type=code&scope=https://www.googleapis.com/auth/sdm.service'
print("Go to this URL to log in:")
print(url)

#code required to generate access token 
code = '4/0AX4XfWhQnrYJHReVljMCdLjabGYq9zkKycSWrlqLeWcqBY0o2kFNzijATv08rzj_8b9Qrw&scope=https://www.googleapis.com/auth/sdm.service'

# current access token, needs to be updated every hour 

access_token = 'Bearer ya29.a0ARrdaM8we8DoEvq48sjS36ORo1dXjUalHqGnoW-tERPUi4g-xISfLdbFsCPviQ6q5GBu5XTsp5z3iPPI5BILsnQg86Ue8UF71QGAidwGGeCCwbCXhS1ZaOBlVXIB2txv5srrqVeaxQa6UGqBUHy8AjbTMeNp'
refresh_token = '1//03gi2kegX0csLCgYIARAAGAMSNwF-L9IrXSAeOscrGsaxZIJoawu4SIMo5kJ-UmLdrzkgBdcVZTDJuEsLi0lY7VaJoIdRpZFS9vw'


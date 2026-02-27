
import requests

CLIENT_ID = '204849' #"YOUR_CLIENT_ID"
CLIENT_SECRET = '04d37eba70e5eeb6eed897ae62860b2b507f1d43' #"YOUR_CLIENT_SECRET"
CODE =  'ef912e5ad8a1b074f3cc2fc9779b38db578ce284' #"PASTE_CODE_HERE"

res = requests.post("https://www.strava.com/oauth/token", data={
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "code": CODE,
    "grant_type": "authorization_code"
})

print(res.json())

#http://localhost/exchange_token?state=&code=ef912e5ad8a1b074f3cc2fc9779b38db578ce284&scope=read,activity:read_all
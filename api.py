import requests
import json
import codecs

def getToken():
  f = open('credentials.json')
  data = json.load(f)
  r = requests.get('http://localhost:8080/oauth2/token', params=data)  
  return r.json()["access_token"]
  
  
def uploadData(token, data):
  access_token = {"access_token": token}
  r = requests.post('http://localhost:8080/api/locations',params=access_token, data = data.encode('utf-8'))
  if r.status_code == 400:
    print(r.json())




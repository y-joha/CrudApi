import requests

BASE = "http://127.0.0.1:5000/"

#response = requests.get(BASE + "Tipol/yohai")
#print(response.json())

#response = requests.get(BASE + "Tipol/shuki")
#print(response.json())

response = requests.put(BASE + "Tipol/yohai" , {"treatment": "needed"})
print(response.json())
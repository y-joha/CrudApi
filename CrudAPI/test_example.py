#https://www.youtube.com/watch?v=GMppyAPbLYk

import requests

BASE = "http://127.0.0.1:5000/"

data = [
    {"name" : "Lion King", "likes": 70000, "views" : 100000},
    {"name" : "HebrewHammer", "likes": 70, "views" : 5000},
    {"name" : "Rahat Lukom The Return", "likes": 6542, "views" : 10},
    {"name" : "Stolen Father", "likes": 700561, "views" : 187},
    {"name" : "Kiss on Forhead", "likes": 35, "views" : 1354},
    {"name" : "Party At The Pool House", "likes": 189, "views" : 17321}]
#response = requests.get(BASE + "Tipol/yohai")
#print(response.json())

#response = requests.get(BASE + "Tipol/shuki")
#print(response.json())

#response = requests.put(BASE + "video/1" , {"likes": 70000,"name" : "yohai", "views" : 100000})
#print(response.json())
#input()

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())    

#input()
#response = requests.delete(BASE + "video/0")
#print(response)
for i in range(len(data)):
    response = requests.get(BASE + "video/" + str(i), data[i])
    print(response.json())


#response = requests.patch(BASE + "video/3", {"views": 69})
#print(response.json())

#response = requests.patch(BASE + "video/2", {"views": 60221023})
#print(response.json())
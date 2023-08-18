import requests
import json
import time
import schedule

i=1
def job():
    url = "https://localhost:7277/api/User/GetUser"

    params={
        'id':'5f660426-ffac-4391-958f-607478e864b4'
    }

    response = requests.get(url,params=params,verify=False)

    if response.status_code==200:
        data=response.json()
        print(data)
    else:
        print("Error:",)

while True:
    job()
    print(i)
    i+=1
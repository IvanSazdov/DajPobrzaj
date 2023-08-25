import requests
from CarsDto import Car
from datetime import datetime
URL = "https://localhost:7115/api/Cars/"


def SendCarsData(cars):
    call = "SendCarsData"

    data = {
        "DateTime":cars.date.isoformat(),  # Sending current time as an example
        "Name": cars.name,  # Replace with your car name
        "Count": cars.count  # Replace with your car count
    }
    r = requests.post(url=URL+call, json=data,verify=False)

    print(r.status_code)

def GetCarsData():
    call = "GetCarsData"

    r= requests.get(url=URL+call,verify=False)

    print(r.content)
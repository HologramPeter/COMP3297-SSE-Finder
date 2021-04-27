# import sys, urllib, pprint, requests, json

# address = sys.argv[1].replace(" ", "%20")
# version = "v1.0.0"

# # remark the version in the geodata for rquesting the data may change into the newer version please update
# response = requests.get("https://geodata.gov.hk/gs/api/" + version + "/locationSearch?q=" + address)

# print("\nResponse status: %d\n"%response.status_code)
# pprint.pprint(response.json())

import requests, json

VERSION = "v1.0.0"

def retrive_Data(location):
    location = location.replace(" ", "%20")
    response = requests.get("https://geodata.gov.hk/gs/api/" + VERSION + "/locationSearch?q=" + location)
    if(response.status_code == 200):
        response = (response.json())[0]
        address = response['addressEN']
        x = response['x']
        y = response['y']
        return(address, x, y)
    else:
        return tuple()


import requests
import json
from config import HOST_IP
"""
初始化shared属性，通过调用token
"""


AUTH_ADDRESS = HOST_IP + "api/auth/login"

DEVICE_ID = "2c53adf0-7797-11ea-aa25-ad673d3fddf6"

auth_data = {"username": "sun_test@qq.com", "password": "123456"}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
shared_address = HOST_IP + "api/plugins/telemetry/DEVICE/" + \
    DEVICE_ID + "/SHARED_SCOPE"

shared_attribute = {
    "P_Range": 32,
    "T_Range": 500,
    "KP_Range": 500,
    "WP_Range": 500,
    "In_Dia": 51,
    "a_Kb": 0.67133,
    "a_Wg": 1.01334,
    "d_Kb": 34.68,
    "d_Wg": 28.56,
    "No_Pipe": "111注汽管网"# 
}

shared_attribute = {
    "Location": "52-14井口",
    "Fluid": "湿蒸汽",
    "Interval": 1,
    "SampleNum": 256,
    "Threshold": 25
}
"""get auth token
"""
r_data = json.dumps(auth_data, indent=4)
print("send json data is {}".format(r_data))
r = requests.post(AUTH_ADDRESS,
                  data=r_data, headers=headers)
print(r.content)
data = json.loads(r.content)
token = data['token']

headers['x-authorization'] = 'Bearer ' + token

r_data = json.dumps(shared_attribute, indent=4)
print("send json data is {}".format(r_data))
r = requests.post(shared_address,
                  data=r_data, headers=headers)
print(r.status_code)

import requests
import json
from json import JSONEncoder
from config import HOST_IP

url = HOST_IP + "api/v1/{}/telemetry"

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}


def post_data(token, data):
    target=url.format(token)
    print("send data to target : {}".format(target))
    r_data=json.dumps(data, indent=4, cls=DataEncoder)
    print("send json data is {}".format(r_data))
    r = requests.post(target,
                      data=r_data, headers=headers)
    print(r.json)

# subclass JSONEncoder
class DataEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

def main():
    token = "cC6jiZZioal0lkAXjIpE"
    data = {'sender': 'Alice', 'receiver': 'Bob', 'message': 'We did it!'}
    post_data(token, data)

if __name__ == "__main__" :
    main()

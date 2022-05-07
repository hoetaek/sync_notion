from os import environ

import requests
import xmltodict

bus_arrival_token = environ["BUS_ARRIVAL_TOKEN"]


def get_bus_arrival_time():
    url = f"http://ws.bus.go.kr/api/rest/arrive/getArrInfoByRoute?serviceKey={bus_arrival_token}&stId=120900042&busRouteId=120900007&ord=06"
    res = requests.get(url)

    xmlstring = res.text
    response_dict = xmltodict.parse(xmlstring)

    return response_dict["ServiceResult"]["msgBody"]["itemList"]["arrmsg1"]

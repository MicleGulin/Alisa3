import requests
from math import sin, cos, sqrt, atan2, radians


import requests

def get_geo_info(city_name, type_info):
    url = "https://geocode-maps.yandex.ru/1.x/"
    params = {
        'geocode': city_name,
        'format': 'json',
        'apikey': "8013b162-6b42-4997-9691-77b7074026e0"
    }

    response = requests.get(url, params)
    data = response.json()

    geo_object = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']

    if type_info == 'coordinates':
        return [float(x) for x in geo_object['Point']['pos'].split(' ')]
    elif type_info == 'country':
        return geo_object['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['CountryName']


def get_distance(p1, p2):
    R = 6373.0

    lon1 = radians(p1[0])
    lat1 = radians(p1[1])
    lon2 = radians(p2[0])
    lat2 = radians(p2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

import requests
from . import keys


def get_long_lat(address):
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    address = address

    params = {
        'key': keys.MapApi.get_key(),
        'address': address
    }
    response = requests.get(base_url, params=params).json()

    if response['status'] == 'OK':
        lat = response['results'][0]['geometry']['location']['lat']
        lng = response['results'][0]['geometry']['location']['lng']
        return lat, lng
    else:
        raise LookupError


def get_directions(*args, **kwargs):
    origin = kwargs['origin']
    destination = kwargs['destination']

    base_url = 'https://maps.googleapis.com/maps/api/directions/json?'
    params = {
        'key': keys.MapApi.get_key(),
        'origin': origin,
        'destination': destination,
    }
    response = requests.get(base_url, params=params).json()
    if response['status'] == 'OK':
        return response
    else:
        raise LookupError


def get_distance(*args, **kwargs):
    origin = kwargs['origin']
    destination = kwargs['destination']

    base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    params = {
        'key': keys.MapApi.get_key(),
        'origin': origin,
        'destination': destination,
        'mode': 'walk'
    }
    response = requests.get(base_url, params=params).json()
    if response['status'] == 'OK':
        result = response['rows']
        for element in result:
            for distance in element['elements']:
                distance_m = distance['distance']['value']
                return distance_m
    else:
        raise LookupError

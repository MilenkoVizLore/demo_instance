""" This file contains all functions that works with coordinates or with Points of Interest. """

import urllib2
import json
import ssl

from math import radians, cos, sin, atan2, sqrt

""" Global variables """
EARTH_RADIUS = 6371500

CLIENT_ID = "PHLMPJ4EJZB2QBQHZG2KUUTNNWZTLW4ZEJRRQI5VW5TLMRMI"
CLIENT_SECRET = "A25MIXXIPP42RD1P4T4PMKZVIYE0OAUHHWX1PPB3YECAFQ4N"

BASE_URL = "https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&limit=50&intent=browse"\
           % (CLIENT_ID, CLIENT_SECRET)


def get_response(url):
    """
    This function is used to make connection to Foursquare API.
    :param url: String representation of URL that user wants to call.
    :return: Return dictionary of venues from Foursquare API
    """
    headers = dict()
    headers['Accept'] = 'application/json'
    request = urllib2.Request(url, None, headers)
    result = urllib2.urlopen(request)
    obj = json.loads(result.read())
    poi = obj['response']['venues']
    return poi


def filter_result(data):
    """
    Filters the result that Foursquare API returned as answer to our request. Filtered result is compatible with POI
    proxy Specific Enabler that can be used to collect data from different online services.
    NOTE: There code is available on https://github.com/alrocar/POIProxy .
    :param data: Dictionary of venues returned from Foursquare API.
    :return: Returns new dictionary containing only one part of information from original response.
    """
    new_data = []
    for poi in data:
        new_data.append({"geometry":
                             {
                                 "coordinates": [poi['location']['lng'], poi['location']['lng']]
                             },
                         "properties":
                             {
                                 "name": poi['name'], "category": poi['categories'][0]['name']
                             }
        })
    return new_data


def radius(lat, lon, distance, categories=None, search=None):
    """
    Defines how to use radius search on Foursquare API. User just needs to provide data, everything else will be
    modified as defined on Foursquare API.
    :param lat: Latitude of center point.
    :param lon: Longitude of center point.
    :param distance: Distance from center point defining a search region.
    :param categories: POI categories that we are interested in.
    :param search: Search term in form of string. NOTE: No spaces!
    :return: Filtered result from Foursquare API.
    """
    if search is None:
        url = BASE_URL + "&radius=%d&v=20150101&ll=%f,%f" % (distance, lat, lon)
    else:
        url = BASE_URL + "&radius=%d&v=20150101&ll=%f,%f&search=%s" % (distance, lat, lon, search)

    if categories is not None:
        url_add = ""
        for cat in categories:
            url_add = url_add + str(cat) + ","

        url = url + "&categoryId=" + url_add
        url = url[:-1]

    poi = get_response(url)
    return filter_result(poi)


def extend(min_x, min_y, max_x, max_y, categories=None, search=None):
    """
    Defines how to use radius search on Foursquare API. User just needs to provide data, everything else will be
    modified as defined on Foursquare API.
    :param min_x: Longitude of South-West point.
    :param min_y: Latitude of South-West point.
    :param max_x: Longitude of North-East point.
    :param max_y: Longitude of North-East point.
    :param categories: POI categories that we are interested in.
    :param search: Search term in form of string. NOTE: No spaces!
    :return: Filtered result from Foursquare API.
    """
    if search is None:
        url = BASE_URL + "&v=20150101&sw=%f,%f&ne=%f,%f" % (min_x, min_y, max_x, max_y)
    else:
        url = BASE_URL + "&v=20150101&sw=%f,%f&ne=%f,%f&search=%s" % (min_x, min_y, max_x, max_y, search)

    if categories is not None:
        url_add = ""
        for cat in categories:
            url_add = url_add + str(cat) + ","

        url = url + "&categoryId=" + url_add
        url = url[:-1]

    poi = get_response(url)
    return filter_result(poi)


def distance_between_gps_coordinates(lat_a, lon_a, lat_b, lon_b):
    """
    Calculate the distance in meters between two GPS points.
    :param lat_a: Latitude of point A.
    :param lon_a: Longitude of point A.
    :param lat_b: Latitude of point B.
    :param lon_b: Longitude of point B.
    :return: Distance between two given points in meters.
    """
    d_lon = radians(lon_b - lon_a)
    d_lat = radians(lat_b - lat_a)
    a = ((sin(d_lat/2)) ** 2) + cos(radians(lat_a)) * cos(radians(lat_b)) * ((sin(d_lon/2)) ** 2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return EARTH_RADIUS * c


def grade_distance(lat_a, lng_a, lat_b, lng_b):
    """
    Gives grades for every distance, smaller distance gives better grade.
    :param lat_a: Latitude of point A.
    :param lng_a: Longitude of point A.
    :param lat_b: Latitude of point B.
    :param lng_b: Longitude of point B.
    :return: Returns grade for given distance.
    """
    distance = distance_between_gps_coordinates(lat_a, lng_a, lat_b, lng_b)
    if distance <= 10:
        return 5
    elif distance <= 50:
        return 3
    elif distance <= 200:
        return 2
    else:
        return 1


def get_poi(lat, lng, radius):
    """
    Search for points of interest on poi data provider, for the given search radius.
    :param lat: Latitude of center point.
    :param lng: Longitude of center point.
    :param radius: Search radius.
    :return: Returns points of interest database provider answer, dictionary of available points of interest in the
    given radius.
    """
    url = 'http://104.154.38.236/poi_dp/radial_search.php?lat=%f&lon=%f&radius=%d' % (lat, lng, radius)
    headers = dict()
    headers['Content-type'] = 'application/json'

    result = None
    try:
        request = urllib2.Request(url, None, headers=headers)
        result = urllib2.urlopen(request, timeout=10).read()
    except:
        return dict()
    poi = json.loads(result)
    if 'pois' in poi and len(poi['pois']) > 0:
        return poi['pois']
    else:
        return dict()
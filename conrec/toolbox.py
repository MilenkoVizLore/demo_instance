import datetime
import urllib2
import json
import operator
import logging

from math import radians, cos, sin, atan2, sqrt

dp = 'p'# development or production
earth_radius = 6371500  # radius of the earth in meters

'''                  Walking          Sitting         Standing             '''
lookup_table = [[[2, 5, 1, 1, 4], [3, 4, 1, 1, 4], [3, 4, 1, 1, 4]], # Morning
                [[4, 2, 5, 1, 1], [4, 1, 3, 1, 1], [5, 1, 4, 1, 1]], # Noon
                [[4, 4, 2, 2, 3], [4, 4, 1, 2, 3], [4, 4, 1, 2, 3]], # Afternoon
                [[3, 1, 5, 4, 4], [2, 1, 4, 4, 4], [2, 1, 4, 4, 4]], # Evening
                [[1, 1, 1, 5, 5], [1, 1, 1, 4, 5], [1, 1, 1, 4, 5]]] # Night
'''               [ Free time, Morning, Lunch, Bar, Transport ]            '''


def get_time_section(milliseconds):
    time = datetime.datetime.fromtimestamp(milliseconds/1000)
    hours = time.hour
    if 11 > hours >= 6:
        return 0  # Morning
    elif 15 > hours >= 11:
        return 1  # Noon
    elif 18 > hours >= 15:
        return 2  # Afternoon
    elif 22 > hours >= 18:
        return 3  # Evening
    else:
        return 4  # Night


def get_curr_activity(prob_lst):
    if float(prob_lst['sitting']) > 0.5:
        return 1
    elif float(prob_lst['walking']) > 0.5:
        return 0
    elif float(prob_lst['standing']) > 0.5:
        return 2
    else:
        2



def get_user_activity(user_id):
    url = 'http://130.211.136.203:8080/ac/?ac=1&uuid=%s&alg=svm&fs=standard&tp=600' % user_id
    headers = dict()
    headers['Accept'] = 'application/json'
    result = None
    try:
        request = urllib2.Request(url, None, headers=headers)
        result = urllib2.urlopen(request).read()
        activity = json.loads(result)
        return activity
    except urllib2.HTTPError, e:
        if e.code == 404 or e.code == 500:
            return 'None'


def distance_between_gps_coordinates(lat_a, lon_a, lat_b, lon_b):
    d_lon = radians(lon_b - lon_a)
    d_lat = radians(lat_b - lat_a)
    a = ((sin(d_lat/2)) ** 2) + cos(radians(lat_a)) * cos(radians(lat_b)) * ((sin(d_lon/2)) ** 2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return earth_radius * c


def get_poi(lat, lng, radius):
    url = 'http://130.211.136.203/poi_dp/radial_search.php?lat=%d&lon=%d&radius=%d' % (lat, lng, radius)
    headers = dict()
    headers['Content-type'] = 'application/json'
    result = None
    try:
        request = urllib2.Request(url, None, headers=headers)
        result = urllib2.urlopen(request).read()
    except urllib2.HTTPError:
        print "error"
        result = None
    poi = json.loads(result)
    return poi['pois']


def decode_category(category):
    if category == 'Entertainment':
        return 0
    elif category == 'Morning':
        return 1
    elif category == 'Lunch':
        return 2
    elif category == 'Club and bar':
        return 3
    elif category == 'Transport':
        return 4
    else:
        return 0


def grade_distance(lat_a, lng_a, lat_b, lng_b):
    distance = distance_between_gps_coordinates(lat_a, lng_a, lat_b, lng_b)
    if distance <= 10:
        return 5
    elif distance <= 50:
        return 3
    elif distance <= 200:
        return 2
    else:
        return 1

def get_recommendation(time_stamp, coordinates, user_id):
    dbalogger = logging.getLogger(__name__)
    if dp == 'p':
        part_of_day = get_time_section(time_stamp)
        act_rest_answer = get_user_activity(user_id)
        activity = get_curr_activity(act_rest_answer['svm_vector'])
    else:
        part_of_day = 0
        act_rest_answer = {'svm_vector': [0.2, 0.1, 0.5, 0.1, 0.1], 'cur_act': 'walking'}
        activity = get_curr_activity(act_rest_answer['svm_vector'])

    points_of_interest = get_poi(coordinates['lat'], coordinates['lon'], 200)
    poi_lst = {}

    ''' Get id of all poi and rate them based on activity, context and distance. '''
    for key, val in points_of_interest.iteritems():
        f_res = lookup_table[part_of_day][activity][decode_category(val['fw_core']['category'])]
        s_res = grade_distance(coordinates['lat'], coordinates['lon'], val['fw_core']['location']['wgs84'][
            'latitude'], val['fw_core']['location']['wgs84']['longitude'])
        poi_lst[key] = f_res * s_res

    ''' Sort pois based on grades and return first 15 elements. '''
    sort_poi_lst = sorted(poi_lst.items(), key=operator.itemgetter(1))
    ret_dict = dict()
    if len(sort_poi_lst) > 15:
        n_it = 15
    else:
        n_it = len(sort_poi_lst)
    for num in range(0, n_it):
        ret_dict[sort_poi_lst[num][0]] = points_of_interest[sort_poi_lst[num][0]]
    return ret_dict
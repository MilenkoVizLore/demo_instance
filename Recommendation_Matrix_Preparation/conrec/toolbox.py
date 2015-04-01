import datetime
import urllib2
import json
import operator

from conrec.models import Ignore
from conrec.poi_module import get_poi, grade_distance

'''                  Walking          Sitting         Standing          Default                  '''
lookup_table = [[[2, 5, 1, 1, 4], [3, 4, 1, 1, 4], [3, 4, 1, 1, 4], [3, 5, 1, 1, 4]],  # Morning
                [[4, 2, 5, 1, 1], [4, 1, 3, 1, 1], [5, 1, 4, 1, 1], [4, 1, 4, 1, 1]],  # Noon
                [[4, 4, 2, 2, 3], [4, 4, 1, 2, 3], [4, 4, 1, 2, 3], [4, 4, 1, 2, 3]],  # Afternoon
                [[3, 1, 5, 4, 4], [2, 1, 4, 4, 4], [2, 1, 4, 4, 4], [2, 1, 4, 4, 4]],  # Evening
                [[1, 1, 1, 5, 5], [1, 1, 1, 4, 5], [1, 1, 1, 4, 5], [1, 1, 1, 4, 5]]]  # Night
'''               [ Free time,    Morning,    Lunch,    Bar,    Transport ]                      '''


def get_time_section(milliseconds):
    """
    Tells as what part of the day is it. Day is split to several sections like: morning, noon, afternoon,
    evening, night. These are predefined by programmer.
    :param milliseconds: Represents current time, in epoch (from January 1, 1970).
    :return: Number representing concrete part of the day. This number is used to reference to lookup table.
    """
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


def get_curr_activity(prob_dict):
    """
    Figure out what category in dictionary of all categories have the best probability.
    :param prob_dict: Dictionary with categories as keys, and probability as values.
    :return: Number representing recognised category. This number is used to reference to lookup table.
    """
    new_prob = sorted(prob_dict.items(), key=operator.itemgetter(1), reverse=True)
    activity = new_prob[0][0]
    if activity == 'walking':
        return 0
    elif activity == 'sitting':
        return 1
    elif activity == 'standing':
        return 2
    else:
        return 3


def decode_activity(act):
    """
    Transforms integer representation of categories to string representation.
    :param act: Number representing one of categories.
    :return: String of recognised activity.
    """
    if act == 0:
        return "walking"
    elif act == 1:
        return "sitting"
    elif act == 2:
        return "standing"
    else:
        return "not recognised"


def get_user_activity(user_id):
    """
    Asks the activity recognition provider what is the current activity for the given user.
    :param user_id: String representation of user unique identification number.
    :return: Returns answer from activity recognition provider.
    """
    url = 'http://130.211.136.203:8080/ac/?ac=1&uuid=%s&alg=svm&fs=standard&tp=600' % user_id
    # url = 'http://89.216.30.67:55555/ac/?ac=1&uuid=%s&alg=svm&fs=standard&tp=600' % user_id
    headers = dict()
    headers['Accept'] = 'application/json'
    result = None

    try:
        request = urllib2.Request(url, None, headers=headers)
        result = urllib2.urlopen(request).read()
        activity = json.loads(result)
        return activity
    except(RuntimeError, TypeError, NameError):
        return {"error": "Could not contact the server"}


def decode_category(category):
    """
    For some given category, already defined by programmer transforms string representation of category to integer
    representation. This integer representation is later used to reference to lookup table.
    :param category: String representation of category.
    :return: Integer representation of the given category.
    """
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


def save_ignored_for_current_user(user_id, poi_id):
    """
    Saves the tuple (user, poi) to local database.
    :param user_id: User identification.
    :param poi_id: POI identification.
    """
    i_poi = Ignore(uuid=user_id, ignored=poi_id)
    i_poi.save()


def get_ignored_for_current_user(user_id):
    """
    Reads what POIs are ignored, from the database.
    :param user_id: User identification.
    :return: List of POI identification, that are already ignored by user.
    """
    lst_ignored = []
    user_exist = Ignore.objects.filter(uuid=user_id).exists()
    if user_exist:
        i_poi = Ignore.objects.all().filter(uuid=user_id)
        for poi in i_poi:
            lst_ignored.append(poi.ignored)
    return lst_ignored


def get_recommendation(time_stamp, coordinates, user_id, ignore):
    """
    Main handler function for recommend.
    :param time_stamp: Time from beginning of the epoch (1.1.1970)
    :param coordinates: Dictionary with coordinates.
    :param user_id: Identification of the current user.
    :param ignore: Identification of POI user ignored from previous recommend.
    :return: Dictionary representing answer for request to recommend.
    """
    ''' Get all required data. '''
    part_of_day = get_time_section(time_stamp)
    act_rest_answer = get_user_activity(user_id)
    if 'error' in act_rest_answer:
        activity = 3  # If activity recognition provider encountered some error.
    else:
        req_act = dict()
        for k, v in act_rest_answer['svm_vector'].iteritems():
            req_act[k] = float(v)
        activity = get_curr_activity(req_act)

    ''' Get all POIs in radius of 300 meters from user. '''
    points_of_interest = get_poi(coordinates['lat'], coordinates['lon'], 300)
    poi_dict = {}

    ''' Get id of all poi and rate them based on activity, context and distance. '''
    for key, val in points_of_interest.iteritems():
        f_res = lookup_table[part_of_day][activity][decode_category(val['fw_core']['category'])]
        s_res = grade_distance(coordinates['lat'], coordinates['lon'], val['fw_core']['location']['wgs84'][
            'latitude'], val['fw_core']['location']['wgs84']['longitude'])
        poi_dict[key] = f_res * s_res

    ''' Slice out ignored. '''
    if ignore != 'None' and ignore in poi_dict:
        save_ignored_for_current_user(user_id, ignore)

    ignored = get_ignored_for_current_user(user_id)
    for ig_poi in ignored:
        if ig_poi in poi_dict:
            del poi_dict[ig_poi]

    ''' Sort POIs based on grades and return first 15 elements. '''
    sort_poi_lst = sorted(poi_dict.items(), key=operator.itemgetter(1), reverse=True)
    ret_dict = {"POIS": [], "activity": decode_activity(activity)}
    if len(sort_poi_lst) > 5:
        n_it = 5
    else:
        n_it = len(sort_poi_lst)
    for num in range(0, n_it):
        ret_dict['POIS'].append({sort_poi_lst[num][0]: points_of_interest[sort_poi_lst[num][0]]})
    return ret_dict

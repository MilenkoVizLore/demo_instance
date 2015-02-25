__author__ = 'luigi'
import urllib2


def test_recommend():
    url = 'http://localhost:8433/recommend/'
    headers = {}
    headers['Content-type'] = 'application/json'
    data = "'uuid': 'an32524fadfkl09jk1', 'lat': 12.458935, 'lng': 24.553212"
    request = urllib2.Request(url, data, headers)
    result = urllib2.urlopen(request).read()
    print result

test_recommend()
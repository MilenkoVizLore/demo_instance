import requests
import json

POI_DP_URL = "http://localhost/poi_dp/"


info = {"fw_core": {"location": {"wgs84": {"latitude": 1.12,
                                           "longitude": 2.23}},
                                "category": "Andrej",
                                "name": {"": "Andrija"},
                                "short_name": {"": "Andarevic"},
                                "label": {"": "Lojdl"},
                                "source": "foursquare"
                    }
        }

inf = {"fw_core": {"location": {"wgs84": {"latitude": 1.982,
                                           "longitude": 2.9863}},
                                "category": "Andr",
                                "name": {"": "Andja"},
                                "short_name": {"": "Aarevic"},
                                "label": {"": "Lojl"},
                                "source": "foursquare"
                }
        }

headers = {'content-type': 'application/json'}
response = requests.post(POI_DP_URL + 'add_poi.php', data=json.dumps(info),
                         headers=headers)

if response.status_code == 200:
    print response.text
else:
    print response.status_code
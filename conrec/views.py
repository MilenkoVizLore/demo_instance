import json

from django.http import HttpResponse
from django.views.generic import View

from conrec.toolbox import get_recommendation


class Recommend(View):
    def get(self, request):
        if 'uuid' in self.request.GET and 'lon' in self.request.GET and 'lat' in self.request.GET \
                and 'ts' in self.request.GET:
            uuid = self.request.GET['uuid']
            lon = float(self.request.GET['lon'])
            lat = float(self.request.GET['lat'])
            ts = int(self.request.GET['ts'])
        else:
            return HttpResponse("Insufficient data provided.")

        if 'ac' in self.request.GET:
            ac = self.request.GET['ac']
            if ac not in ['0', '1', '2', '3']:
                ac = 0
            else:
                ac = int(ac)
        else:
            ac = 0

        # Get poi_num param for final version.
        #
        # ------------------------------------

        dict_res = get_recommendation(ts, {'lat': lat, 'lon': lon}, uuid)
        return HttpResponse(json.dumps(dict_res), content_type="application/json")

    def post(self, request):
        data = 'Use GET method instead.'
        return HttpResponse(data)

class Test(View):
    def
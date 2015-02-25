from django.http import HttpResponse
from django.views.generic import View


class Recommend(View):
    def get(self, request):
        return HttpResponse('Only POST method is enabled.')

    def post(self, request):
        data = "{'uuid': 'an284lo918gjsi472', 'name': 'Test POI', 'lat': 34.874328, 'lng': 2.498823}"
        return HttpResponse(data)
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def HomeView(request):
	return render_to_response("index.html", None, context_instance=RequestContext(request))
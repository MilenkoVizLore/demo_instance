from django.conf.urls import patterns, include, url
from django.contrib import admin
from page.views import HomeView

urlpatterns = patterns('',
                       url(r'^$', HomeView))
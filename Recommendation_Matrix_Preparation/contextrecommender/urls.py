from django.conf.urls import patterns, include, url
from django.contrib import admin
from conrec.views import Recommend, Test

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^recommend/', Recommend.as_view()),
    url(r'^test/', Test.as_view())
)

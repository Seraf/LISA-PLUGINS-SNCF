from django.conf.urls import patterns, url
from SNCF.web import views

urlpatterns = patterns('',
    url(r'^widget$', views.getTraffic, name='getTraffic'),
)

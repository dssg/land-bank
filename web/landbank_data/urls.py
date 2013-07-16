from django.conf.urls import patterns, url

from landbank_data import views

urlpatterns = patterns('',
    url(r'^(?P<search_pin>\d{14})/$', views.pin, name='pin'),
    url(r'^(?P<search_pin>.*)$', views.pin, name='bad_pin')
)

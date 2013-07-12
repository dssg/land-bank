#from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from tastypie.api import Api
from landbank_data.api import ParcelResource

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(ParcelResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'landbank.views.home', name='home'),
    # url(r'^landbank/', include('landbank.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'api/', include(v1_api.urls)),
)

#from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from tastypie.api import Api
from landbank_data.api import ParcelResource, AuctionResource, CashFinResource, ForeclosureResource, MortgageResource, ScavengerResource, TransactionResource

dajaxice_autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(ParcelResource())
v1_api.register(AuctionResource())
v1_api.register(CashFinResource())
v1_api.register(ForeclosureResource())
v1_api.register(MortgageResource())
v1_api.register(ScavengerResource())
v1_api.register(TransactionResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'landbank.views.home', name='home'),
    # url(r'^landbank/', include('landbank.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^$', 'landbank_data.views.home', name='home'),
    url(r'^pin/', include('landbank_data.urls')),
    url(r'^commarea/(?P<search_commarea>[0-9]+)/$', 'landbank_data.views.commarea'),
    url(r'^ward/(?P<search_ward>[0-9]+)/$', 'landbank_data.views.ward'),
    url(r'^tract/(?P<search_tract>[0-9]+)/$', 'landbank_data.views.tract'),
    url(r'^municipality/(?P<search_muni>[a-z_A-Z]+)/$', 'landbank_data.views.municipality'),
    url(r'^(?P<search_pin>\d{14})/$', 'landbank_data.views.pin', name='pin'),
    url(r'search/', 'landbank_data.views.search', name='search'),
    url(r'dajax_test/', 'landbank_data.views.dajax_test', name='dajax_test'),
    url(r'api/', include(v1_api.urls)),
)

urlpatterns += staticfiles_urlpatterns()

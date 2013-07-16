#from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url
from tastypie.api import Api
from landbank_data.api import ParcelResource, AuctionResource, CashFinResource, ForeclosureResource, MortgageResource, ScavengerResource, TransactionResource

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
    (r'^pin/', include('landbank_data.urls')),
    (r'api/', include(v1_api.urls)),
)

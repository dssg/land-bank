import random
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.db import connection
from models import Assessor, CommunityArea, Ward, CensusTract, Municipality, IndicatorCache
from django.core import serializers

@dajaxice_register
def randomize(request):
    dajax = Dajax()
    dajax.assign('#result', 'value', random.randint(1,10))
    dajax.add_data('foo', 'randomize_callback')
    return dajax.json()

@dajaxice_register
def get_property_from_latlng(request, lat, lng):
    lat = str(lat)
    lng = str(lng)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM latlng_to_pin14(" + lat + ", " + lng + ");")
    fetched_pin = cursor.fetchone()[0]
    try: data = serializers.serialize('json', Assessor.objects.filter(pin__exact=fetched_pin)) 
    except: data = None
    dajax = Dajax()
    #dajax.add_data(data, 'pin_callback')
    dajax.redirect('/pin/'+fetched_pin, delay=0)
    return dajax.json()

all_geographies = {
    'communityarea':{
        'name':'Community Area'
        ,'fields':['area_number','area_name']
        ,'headers':['#','Area Name']
        ,'queryset':CommunityArea.objects.all()
    },'ward':{ 
        'name':'Ward'
        ,'fields':['ward','alderman']
        ,'headers':['#','Alderman']
        ,'queryset':Ward.objects.all()
    },'municipality':{ 
        'name':'Municipality'
        ,'fields':['name']
        ,'headers':['Municipality']
        ,'queryset':Municipality.objects.all()
    },'censustract':{ 
        'name':'Census Tract'
        ,'fields':['fips']
        ,'headers':['FIPS Tract ID']
        ,'queryset':CensusTract.objects.all()
    }}
indicator_fields = ['foreclosure_rate','vacancy_usps','med_inc']
indicator_headers = ['Foreclosure Rate','Vacancy Rate','Median Income']

@dajaxice_register
def area_data_table(request, area_type):
    try: geography = all_geographies[area_type]
    except: return 'invalid area_type!'
    headers = geography['headers'] + indicator_headers
    area_qs = geography['queryset'].values('id',**geography['fields'])
    data_obj = {}

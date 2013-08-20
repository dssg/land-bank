import random
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.db import connection
from models import Assessor
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
    dajax.add_data(data, 'onGotPropertyData')
    #dajax.add_data(fetched_pin, 'onGotPropertyData')
    #dajax.redirect('/pin/'+fetched_pin, delay=0)
    return dajax.json()

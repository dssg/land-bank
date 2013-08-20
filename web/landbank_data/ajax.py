import random
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.db import connection
from models import Assessor
from django.core import serializers
from landbank_data.util import sqltodict
from django.contrib.gis.geos import GEOSGeometry

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
    data = {}
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM latlng_to_pin14(" + lat + ", " + lng + ");")
    fetched_pin = cursor.fetchone()[0]
    try:
        assessor = Assessor.objects.get(pin__exact=fetched_pin).__dict__
        assessor.pop('_state',None)
        assessor.pop('loc',None)
        data['assessor'] = assessor
        q = "SELECT * FROM parcel_with_data WHERE pin='" + fetched_pin + "';"
        result = sqltodict(q,None)[0]
        result.pop('wkb_geometry', None)
        data['parcel_info'] = result
    except:
        data['status'] = 'error' 
    dajax = Dajax()
    dajax.add_data(data, 'onGotParcelData')
    return dajax.json()

from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from landbank_data.models import \
  Assessor, PinAreaLookup, CommunityAreas, \
  CensusTract, Wards, Transaction, TractScores, AreaPlotCache
import datetime
import numpy as np
from pytz import timezone
import json

def home(request):
    return render(request, 'landbank_data/home.html', {})

def base_map(request):
    return render(request, 'landbank_data/base_map.html', {})

def map(request, ca_number=1):
    #ca = CommunityAreas.objects.filter(pk__lte=10)
    ca = CommunityAreas.objects.get(area_number=ca_number)
    ca.geom.transform(4326)
    ca_list = []
    ca_list.append(ca)
    #for c in ca:
        #c.geom.transform(4326)
        #ca_list.append(c)
    return render(request, 'landbank_data/map.html', {'object_list': ca_list})

def pin(request, search_pin=None):
    try: 
      search_assessor = Assessor.objects.get(pin=search_pin)
      mapcenter       = {'lon': search_assessor.long_x, 'lat': search_assessor.lat_y}
    except Assessor.DoesNotExist: 
      search_assessor = None
      mapcenter       = {'lon': -87.65, 'lat': 41.85}
    else:  
      lookup = PinAreaLookup.objects.get(pin=search_pin)

    try:      ward = Wards.objects.get(pk=lookup.ward_id)
    except:   ward = None

    try:      ca = CommunityAreas.objects.get(pk=lookup.community_area_id)
    except:   ca = None

    try:      tract = CensusTract.objects.get(pk=lookup.census_tract_id)
    except:   tract = None

    try:      score = TractScores.objects.get(census_tract_id=lookup.census_tract_id)
    except:   score = None

    try:
      apc = AreaPlotCache.objects.\
        filter(area_type__exact='Community Area').\
        filter(area_id__exact=ca.id)[:1][0]
      histData = apc.json_str
    except:   histData = '""'

    # Todo: debug this; doesn't seem to work
    try:      brown = Brownfield.objects.get(pin=bigint(lookup.pin))
    except:   brown = None

    return render(request, 'landbank_data/pin.html', {\
	 'assessor': search_assessor\
	,'ward': ward\
	,'ca': ca\
	,'tract': tract\
	,'score': score\
        ,'brown': brown\
        ,'mapcenter': mapcenter\
        ,'histData': histData\
	})

def commarea(request, search_commarea=None):
  commarea = get_object_or_404(CommunityAreas,area_number=search_commarea)

  apc = AreaPlotCache.objects.\
    filter(area_type__exact='Community Area').\
    filter(area_id__exact=commarea.id)[0]
  outline = commarea.geom
  outline.transform(4326)
  mapcenter_centroid = outline.centroid
  mapcenter = {'lon': mapcenter_centroid[0], 'lat': mapcenter_centroid[1]}
  proplist = [\
    {'key': 'Type', 'val': 'Chicago community area'},\
    {'key': 'Number', 'val': commarea.area_number}\
  ]
  
#  print data
  return render_to_response('aggregate_geom.html', {\
    'histData': apc.json_str,\
    'title': commarea.area_name.title(),\
    'proplist': proplist,\
    'mapcenter': mapcenter,\
    'outline': outline
    },\
    context_instance=RequestContext(request))


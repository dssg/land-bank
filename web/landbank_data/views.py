from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from landbank_data.models import \
  Assessor, PinAreaLookup, CommunityArea, \
  CensusTract, Ward, Transaction, TractScores, AreaPlotCache,\
  CensusTractMapping, IndicatorCache
import datetime
import numpy as np
from pytz import timezone
import json

def home(request):
    return render(request, 'landbank_data/home.html', {})

def base_map(request):
    return render(request, 'landbank_data/base_map.html', {})

def map(request, ca_number=1):
    #ca = CommunityArea.objects.filter(pk__lte=10)
    ca = CommunityArea.objects.get(area_number=ca_number)
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

    try:      ward = Ward.objects.get(pk=lookup.ward_id)
    except:   ward = None

    try:      ca = CommunityArea.objects.get(pk=lookup.community_area_id)
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
  # First get the community area.
  commarea = get_object_or_404(CommunityArea,area_number=search_commarea)
  # Now get a bunch of indicator values for it.
  indicators = IndicatorCache.objects.filter(area_type__exact='Community Area').\
    filter(area_id__exact=commarea.id)
  pop = int(indicators.get(indicator_name='pop').indicator_value)
  pct_white = indicators.get(indicator_name='pct_whitenh').indicator_value
  pct_black = indicators.get(indicator_name='pct_blacknh').indicator_value
  pct_asian = indicators.get(indicator_name='pct_asiannh').indicator_value
  pct_hispanic = indicators.get(indicator_name='pct_hispanic').indicator_value
  median_age = indicators.get(indicator_name='median_age').indicator_value
  pct_owner_occupied = indicators.get(indicator_name='pct_owner_occupied').indicator_value

  # Now make the histograms for comparing it to other community areas.
  # These could be cached.
  median_ages = [i.indicator_value for i in \
    IndicatorCache.objects.filter(area_type__exact='Community Area').\
                           filter(indicator_name__exact='median_age').\
                           filter(indicator_value__gt=0)]
  median_ages_values, median_ages_bins = \
    np.histogram(median_ages,bins=10) 

  pct_owner_occupieds = [i.indicator_value for i in \
    IndicatorCache.objects.filter(area_type__exact='Community Area').\
                           filter(indicator_name__exact='pct_owner_occupied').\
                           filter(indicator_value__gt=0)]
  pct_owner_occupieds_values, pct_owner_occupieds_bins = \
    np.histogram(pct_owner_occupieds,bins=10) 

  # Get the data ready to be passed to the plotter.
  histData = [\
    {'data': [{'x': b, 'y': v} for b,v in \
      zip(median_ages_bins,median_ages_values)],\
     'title': 'Median age', 'marker': median_age},\
    {'data': [{'x': b, 'y': v} for b,v in \
      zip(pct_owner_occupieds_bins,pct_owner_occupieds_values)],\
     'title': 'Percent owner occupied', 'marker': pct_owner_occupied}\
  ]

  # Make the outline of the community area for the map.
  outline = commarea.geom
  outline.transform(4326)
  mapcenter_centroid = outline.centroid
  mapcenter = {'lon': mapcenter_centroid[0], 'lat': mapcenter_centroid[1]}

  # These are the indicators to show at the top of the page.
  proplist = [\
    {'key': 'Type', 'val': 'Chicago community area'},\
    {'key': 'Number', 'val': commarea.area_number},\
    {'key': 'Population', 'val': pop},\
    {'key': 'White', 'val': '%4.1f%%' % (pct_white)},\
    {'key': 'Black', 'val': '%4.1f%%' % (pct_black)},\
    {'key': 'Hispanic', 'val': '%4.1f%%' % (pct_hispanic)},\
    {'key': 'Asian', 'val': '%4.1f%%' % (pct_asian)},\
  ]
  
  # And we're ready to render.
  return render_to_response('aggregate_geom.html', {\
    'title': commarea.area_name.title(),\
    'proplist': proplist,\
    'mapcenter': mapcenter,\
    'outline': outline,\
    'histData': histData\
    },\
    context_instance=RequestContext(request))


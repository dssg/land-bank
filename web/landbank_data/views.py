from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from landbank_data.models import \
  Assessor, PinAreaLookup, CommunityArea, \
  CensusTract, Ward, Transaction, TractScores, AreaPlotCache,\
  CensusTractMapping, IndicatorCache
import datetime
import numpy as np
from pytz import timezone
import json
import re
from indicator_utils import *

re_fips = re.compile('17031[0-9]{6}')
re_pin = re.compile('[0-9]{14}')
re_ward = re.compile('[wW][aA][rR][dD]')
re_area = re.compile('[aA][rR][eE][aA].*([1-7][0-9]|[1-9])')
re_num = re.compile('[0-9]+')

@csrf_protect
def home(request):
    return render_to_response('landbank_data/home.html', {}, RequestContext(request))
#    return render(request, 'landbank_data/home.html', {})

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

@csrf_protect
def search(request):
    if request.method == "POST":
        search_term = request.POST['search']
        if re.match(re_pin, search_term):
	    url = '/pin/' + search_term
            return redirect(url)
	if re.match(re_fips, search_term):
	    url = '/tract/' + search_term
	    return redirect(url)
	if re.match(re_area, search_term):
	    match = re.search(re_num, search_term)
	    if match is not None:
	        area_number = match.group(0)
                url = '/commarea/' + area_number 
		# TODO: check if area_number is 1-77, if not, give 404
	        return redirect(url)
	if re.match(re_ward, search_term):
	    match = re.search(re_num, search_term)
	    if match is not None:
	        ward_number = match.group(0)
                url = '/ward/' + ward_number 
		# TODO: check if ward_number is 1-50, if not, give 404
	        return redirect(url)

        return render_to_response('landbank_data/test_search.html', {'data': search_term}, RequestContext(request))
    else:
        return render(request, 'landbank_data/home.html', {})

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
  commarea = get_object_or_404(CommunityArea,area_number=search_commarea)
  return aggregate(request, commarea, commarea.area_name.title(), 'Community Area')

def ward(request, search_ward=None):
  ward = get_object_or_404(Ward,ward=search_ward)
  return aggregate(request, ward, 'Chicago '+str(search_ward), 'Ward')

def tract(request, search_tract=None):
  tract = get_object_or_404(CensusTract,fips=search_tract)
  return aggregate(request, tract, str(search_tract), 'Census Tract')

def municipality(request, search_muni=None):
  mymuni=search_muni.replace('_',' ').title()
  muni = get_object_or_404(Municipality,name=mymuni)
  return aggregate(request, muni, mymuni, 'Municipality')

def aggregate(request, search_geom, search_geom_name, geom_type):
  # First get the community area.
  # Now get a bunch of indicator values for it.
  indicators = IndicatorCache.objects.\
    filter(area_type__exact=geom_type).\
    filter(area_id__exact=search_geom.id)

  # Basic demographics
  pop = int(indicators.get(indicator_name='pop').indicator_value)
  pct_white = indicators.get(indicator_name='pct_whitenh').indicator_value
  pct_black = indicators.get(indicator_name='pct_blacknh').indicator_value
  pct_asian = indicators.get(indicator_name='pct_asiannh').indicator_value
  pct_hispanic = indicators.get(indicator_name='pct_hispanic').indicator_value
  median_age = indicators.get(indicator_name='median_age').indicator_value
  pct_owner_occupied = indicators.get(indicator_name='pct_owner_occupied').\
    indicator_value
  segregation = indicators.get(indicator_name='segregation').indicator_value
  owner_occ_hh_size = indicators.get(indicator_name='owner_occ_hh_size').\
    indicator_value
  renter_occ_hh_size = indicators.get(indicator_name='renter_occ_hh_size').\
    indicator_value
  pct_occ_units = indicators.get(indicator_name='pct_occ_units').\
    indicator_value

  # Income
  inc_levels = [\
    'inc_lt_10', 'inc_10_15', 'inc_15_25', 'inc_25_35',\
    'inc_35_50', 'inc_50_75', 'inc_75_100', 'inc_100_150',\
    'inc_150_200', 'inc_gt_200']
  inc_vals = [5,12.5,20,30,42.5,62.5,87.5,125,175,250]
  inc_data = []
  for inc_val, inc_level in zip(inc_vals, inc_levels):
    val = indicators.get(indicator_name=inc_level).indicator_value
    inc_data.append({'x': inc_val, 'y': val})
  med_inc = indicators.get(indicator_name='med_inc').indicator_value/1000.0

  # Now make the histograms for comparing it to other community areas.
  # These could be cached.
  pct_owner_occupieds_values, pct_owner_occupieds_bins = \
    indicator_hist(geom_type, 'pct_owner_occupied')
  pct_occ_units_values, pct_occ_units_bins = \
    indicator_hist(geom_type, 'pct_occ_units')
  segregations_values, segregations_bins = \
    indicator_hist(geom_type, 'segregation')
  owner_occ_hh_sizes_values, owner_occ_hh_sizes_bins = \
    indicator_hist(geom_type, 'owner_occ_hh_size')
  renter_occ_hh_sizes_values, renter_occ_hh_sizes_bins = \
    indicator_hist(geom_type, 'renter_occ_hh_size')
  median_ages_values, median_ages_bins = \
    indicator_hist(geom_type, 'median_age')

  # Get the data ready to be passed to the plotter.
  histData = {\
    ('Demographics','Black lines mark this '+geom_type+' relative to all others') : [\
    {'data': [{'x': b, 'y': v} for b,v in \
      zip(pct_owner_occupieds_bins,pct_owner_occupieds_values)],\
     'title': 'Percent owner occupied', 'marker': pct_owner_occupied,\
     'tooltip': 'Percent owner occupied housing units'},
    {'data': [{'x': b, 'y': v} for b,v in \
      zip(pct_occ_units_bins,pct_occ_units_values)],\
     'title': 'Percent occupied units', 'marker': pct_occ_units,\
     'tooltip': 'Percent housing units that are occupied'},\
    {'data': [{'x': b, 'y': v} for b,v in \
      zip(owner_occ_hh_sizes_bins,owner_occ_hh_sizes_values)],\
     'title': 'Household size, owner-occupied', 'marker': owner_occ_hh_size,\
     'tooltip': 'Average household size in owner-occupied units'},\
    {'data': [{'x': b, 'y': v} for b,v in \
      zip(renter_occ_hh_sizes_bins,renter_occ_hh_sizes_values)],\
     'title': 'Household size, renter-occupied', 'marker': renter_occ_hh_size,\
     'tooltip': 'Average household size in renter-occupied units'},\
    {'data': [{'x': b, 'y': v} for b,v in \
      zip(segregations_bins,segregations_values)],\
     'title': 'Segregation', 'marker': segregation,\
     'tooltip': 'Percentage of people who would have to move '+\
       'out for its racial and ethnic '+\
       'composition to match the city as a whole'},\
    {'data': [{'x': b, 'y': v} for b,v in \
      zip(median_ages_bins,median_ages_values)],\
     'title': 'Median age', 'marker': median_age, \
     'tooltip': 'Median age of residents'}],\
    ('Income','Black line marks median household income') : [\
    {'title': 'Household income (thousands)', 'marker': med_inc,\
     'tooltip': 'Annual household income in thousands of dollars', 'data': inc_data}]\
}

  # Make the outline of the community area for the map.
  outline = search_geom.loc if geom_type == "Census Tract" else search_geom.geom
  outline.transform(4326)
  mapcenter_centroid = outline.centroid
  mapcenter = {'lon': mapcenter_centroid[0], 'lat': mapcenter_centroid[1]}

  # These are the indicators to show at the top of the page.
  proplist = [\
    {'key': 'Type', 'val': geom_type},\
    {'key': 'Population', 'val': pop},\
    {'key': 'White', 'val': '%4.1f%%' % (pct_white)},\
    {'key': 'Black', 'val': '%4.1f%%' % (pct_black)},\
    {'key': 'Hispanic', 'val': '%4.1f%%' % (pct_hispanic)},\
    {'key': 'Asian', 'val': '%4.1f%%' % (pct_asian)},\
  ]
  
  # And we're ready to render.
  return render_to_response('aggregate_geom.html', {\
    'title': search_geom_name,\
    'type': geom_type,\
    'proplist': proplist,\
    'mapcenter': mapcenter,\
    'outline': outline,\
    'histData': histData\
    },\
    context_instance=RequestContext(request))


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
    return render_to_response('landbank_data/leaflet.html', {}, RequestContext(request))
#    return render(request, 'landbank_data/home.html', {})

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
                url = '/communityarea/' + area_number 
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
    try:      brown = Brownfield.objects.get(pin=lookup.pin)
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

def communityarea(request, search_communityarea=None):
  communityarea = get_object_or_404(CommunityArea,area_number=search_communityarea)
  return aggregate(request, communityarea, communityarea.area_name.title(), 'Community Area')

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

def fetch_indicators_and_hists(search_geom, search_geom_name, geom_type, city_flag):
  retval = {}
  indicators = IndicatorCache.objects.\
    filter(area_type__exact=geom_type).\
    filter(area_id__exact=search_geom.id)

  ind_list = [\
    'pop', 'pct_whitenh', 'pct_blacknh', 'pct_asiannh', 'pct_hispanic',\
    'pct_sfh', 'pct_condo', 'pct_multifamily', 'pct_commind', \
    'median_age', 'pct_owner_occupied', 'segregation', \
    'owner_occ_hh_size', 'renter_occ_hh_size', 'pct_occ_units',\
    'med_inc', 'inc_lt_10', 'inc_10_15', 'inc_15_25', 'inc_25_35',\
    'inc_35_50', 'inc_50_75', 'inc_75_100', 'inc_100_150',\
    'inc_150_200', 'inc_gt_200', 'jobs_within_mile_pc',\
    'vacancy_usps', 'foreclosure_rate', 'median_price', \
    'transactions_per_thousand', 'mortgages_per_thousand', \
    'percent_lowvalue', 'percent_businessbuyers']
  if city_flag: ind_list = ind_list + [\
    'construction_pc', 'demolitions_pc', 'vacancy_311']

  for indicator_name in ind_list:
    iv = indicators.\
      filter(indicator_name__exact=indicator_name)
    thisind = iv[0].indicator_value
    if len(iv) > 1: 
      thisind = iv.latest('indicator_date').indicator_value
    hist_range = None
    if indicator_name=='transactions_per_thousand': hist_range=(0,25)
    elif indicator_name=='mortgages_per_thousand': hist_range=(0,25)
    elif indicator_name=='median_price': hist_range=(0,1000000)
    elif indicator_name=='jobs_within_mile_pc': hist_range=(0,5)
    elif indicator_name=='construction_pc': hist_range=(0,1000)
    vals, bins, score = indicator_hist(geom_type, indicator_name, \
      thisind, hist_range=hist_range)
    if indicator_name=='demolitions_pc':
      retval[indicator_name] = {\
        'indicator': thisind*1000,\
        'score': str(int(score)),\
        'hist': [{'x': b, 'y': v} for b,v in zip([i*1000 for i in bins], vals)] }
    else:
      retval[indicator_name] = {\
        'indicator': thisind,\
        'score': str(int(score)),\
        'hist': [{'x': b, 'y': v} for b,v in zip(bins, vals)] }

  inc_levels = ['inc_lt_10', 'inc_10_15', 'inc_15_25', 'inc_25_35',\
    'inc_35_50', 'inc_50_75', 'inc_75_100', 'inc_100_150',\
    'inc_150_200', 'inc_gt_200']
  inc_vals = [5,12.5,20,30,42.5,62.5,87.5,125,175,250]
  inc_data = []
  for inc_val, inc_level in zip(inc_vals, inc_levels):
    inc_data.append({'x': inc_val, 'y': retval[inc_level]['indicator']})
  retval['income_dist'] = {'hist': inc_data }

  return retval

def aggregate(request, search_geom, search_geom_name, geom_type):
  city_flag=True
  if geom_type=='Municipality' and search_geom_name!='Chicago': city_flag=False
  if geom_type=='Census Tract':
    city_geom=Municipality.objects.get(name='Chicago').geom
    if city_geom.intersection(search_geom.loc).area==0: city_flag=False

  inds = fetch_indicators_and_hists(search_geom, search_geom_name, geom_type, city_flag)
  demographics_hist_dicts = [\
    {'data': inds['pct_owner_occupied']['hist'],\
     'title': 'Owner occupancy rank: '+inds['pct_owner_occupied']['score'],\
     'label': 'Percent owner occupied', 'marker': inds['pct_owner_occupied']['indicator'],\
     'tooltip': 'Percent owner occupied housing units'},
    {'data': inds['pct_occ_units']['hist'],\
     'title': 'Occupancy rank: '+inds['pct_occ_units']['score'],\
     'label': 'Percent occupied units',\
     'marker': inds['pct_occ_units']['indicator'],\
     'tooltip': 'Percent housing units that are occupied'},\
    {'data': inds['owner_occ_hh_size']['hist'],\
     'title': 'Owner crowding rank: '+inds['owner_occ_hh_size']['score'],\
     'label': 'Household size, owner-occupied',\
     'marker': inds['owner_occ_hh_size']['indicator'],\
     'tooltip': 'Average household size in owner-occupied units'},\
    {'data': inds['renter_occ_hh_size']['hist'],\
     'title': 'Renter crowding rank: '+inds['renter_occ_hh_size']['score'],\
     'label': 'Household size, renter-occupied', \
     'marker': inds['renter_occ_hh_size']['indicator'],\
     'tooltip': 'Average household size in renter-occupied units'},\
    {'data': inds['segregation']['hist'],\
     'title': 'Segregation rank: '+inds['segregation']['score'],\
     'label': 'Segregation', 'marker': inds['segregation']['indicator'],\
     'tooltip': 'Percentage of people who would have to move '+\
       'out for its racial and ethnic '+\
       'composition to match the city as a whole'},\
    {'data': inds['median_age']['hist'],\
     'title': 'Median age rank: '+inds['median_age']['score'],\
     'label': 'Median age', \
     'marker': inds['median_age']['indicator'], \
     'tooltip': 'Median age of residents'}\
  ]
  income_hist_dicts = [\
    {'title': 'Household income', \
     'label': 'Household income (thousands)', \
     'tooltip': 'Annual household income in thousands of dollars',\
     'data': inds['income_dist']['hist']},\
    {'title': 'Job access rank: '+inds['jobs_within_mile_pc']['score'],\
     'label': 'Jobs within 1 mile per capita', \
     'marker': inds['jobs_within_mile_pc']['indicator'],\
     'tooltip': 'Jobs within 1 mile of this geometry, per capita', \
     'data': inds['jobs_within_mile_pc']['hist']}]
  if city_flag:
    income_hist_dicts.append( 
    {'title': 'Construction rank: '+inds['construction_pc']['score'],\
     'label': 'Construction spending per capita', \
     'marker': inds['construction_pc']['indicator'],\
     'tooltip': 'Spending on permitted construction per capita', \
     'data': inds['construction_pc']['hist']})

  vacancy_hist_dicts = [\
    {'title': 'USPS vacancy rank: '+inds['vacancy_usps']['score'],\
     'label': 'USPS vacancy rate', \
     'marker': inds['vacancy_usps']['indicator'],\
     'tooltip': 'USPS percentage of vacant/no-stat residential addresses', \
     'data': inds['vacancy_usps']['hist']}]
  if city_flag:
    vacancy_hist_dicts.append({\
     'title': 'Vacancy complaint rank: '+inds['vacancy_311']['score'],\
     'label': 'Vacancy complaint percentage', \
     'marker': inds['vacancy_311']['indicator'],\
     'tooltip': 'Percentage of buildings with 311 vacant building complaints', \
     'data': inds['vacancy_311']['hist']})
    vacancy_hist_dicts.append({\
     'title': 'Demolition rank: '+inds['demolitions_pc']['score'],\
     'label': 'Demolition permits per 1000 residents', \
     'marker': inds['demolitions_pc']['indicator'],\
     'tooltip': 'Demolition permits per 1000 residents', \
     'data': inds['demolitions_pc']['hist']})

  market_hist_dicts = [\
    {'title': 'Foreclosure rank: '+inds['foreclosure_rate']['score'],\
     'label': 'Foreclosure rate', \
     'marker': inds['foreclosure_rate']['indicator'],\
     'tooltip': 'Foreclosures per thousand residential properties (single-family and condo, prev. quarter)',\
     'data': inds['foreclosure_rate']['hist']},\
    {'title': 'Price rank: '+inds['median_price']['score'],\
     'label': 'Median price', 
     'marker': inds['median_price']['indicator'],\
     'tooltip': 'Median price for residential properties (single-family and condo, prev. quarter)',\
     'data': inds['median_price']['hist']},\
    {'title': 'Velocity rank: '+inds['transactions_per_thousand']['score'],\
     'label': 'Transactions per thousand', \
     'marker': inds['transactions_per_thousand']['indicator'],\
     'tooltip': 'Transactions per thousand residential properties (single-family and condo, prev. quarter)',\
     'data': inds['transactions_per_thousand']['hist']},\
    {'title': 'Credit availability rank: '+inds['mortgages_per_thousand']['score'],\
     'label': 'Mortgages per thousand', \
     'marker': inds['mortgages_per_thousand']['indicator'],\
     'tooltip': 'Mortgages per thousand residential properties (single-family and condo, prev. quarter)',\
     'data': inds['mortgages_per_thousand']['hist']},\
    {'title': 'Low-value rank: '+inds['percent_lowvalue']['score'],\
     'label': 'Percent low-value transactions', \
     'marker': inds['percent_lowvalue']['indicator'],\
     'tooltip': 'Percent residential transactions for <$20k (single-family and condo, prev. quarter)',\
     'data': inds['percent_lowvalue']['hist']},\
    {'title': 'Speculation rank: '+inds['percent_businessbuyers']['score'],\
     'label': 'Percent business buyers', \
     'marker': inds['percent_businessbuyers']['indicator'],\
     'tooltip': 'Percent business buyers (single-family and condo, prev. quarter)',\
     'data': inds['percent_businessbuyers']['hist']}\
    ]
  market_timestream_dicts = [\
    {'title': 'Foreclosure rate', 'label': 'Foreclosure rate',\
     'tooltip': 'Foreclosures per thousand residential properties by quarter', \
     'data': indicator_timestream(geom_type, search_geom.id, 'foreclosure_rate')},\
    {'title': 'Median price', \
     'tooltip': 'Median price for residential properties by quarter', \
     'data': indicator_timestream(geom_type, search_geom.id, 'median_price')},\
    {'title': 'Transactions per thousand', \
     'tooltip': 'Transactions per thousand residential properties by quarter', \
     'data': indicator_timestream(geom_type, search_geom.id, 'transactions_per_thousand')},\
    {'title': 'Mortgages per thousand', \
     'tooltip': 'Mortgages per thousand residential properties by quarter', \
     'data': indicator_timestream(geom_type, search_geom.id, 'mortgages_per_thousand')},\
    {'title': 'Percent low-value transactions', \
     'tooltip': 'Percent residential transactions for <$20k by quarter', \
     'data': indicator_timestream(geom_type, search_geom.id, 'percent_lowvalue')},\
    {'title': 'Percent business buyers', \
     'tooltip': 'Percent business buyers by quarter', \
     'data': indicator_timestream(geom_type, search_geom.id, 'percent_businessbuyers')}\
  ]

  # Get the data ready to be passed to the plotter.
  histData = [\
    {('Demographics','Black lines mark this '+geom_type+' relative to all others') : \
    demographics_hist_dicts },\
    {('Income','Black lines mark this '+geom_type+' relative to all others') : \
    income_hist_dicts },\
    {('Real estate market', 'Black lines mark this '+geom_type+' relative to all others') : \
    market_hist_dicts },\
    {('Vacancy and demolition', 'Black lines mark this '+geom_type+' relative to all others') : \
    vacancy_hist_dicts }\
  ]
  timestreamData = [
    {('Real estate market', 'Historical indicators') : \
    market_timestream_dicts }\
  ]

  # Make the outline of the community area for the map.
  outline = search_geom.loc if geom_type == "Census Tract" else search_geom.geom
  outline.transform(4326)
  mapcenter_centroid = outline.centroid
  mapcenter = {'lon': mapcenter_centroid[0], 'lat': mapcenter_centroid[1]}

  # These are the indicators to show at the top of the page.
  proplist = [\
    {'key': 'Type', 'val': geom_type},\
    {'key': 'Population', 'val': inds['pop']['indicator']},\
    {'key': 'BR', 'val': ''},\
    {'key': 'White', 'val': '%4.1f%%' % (inds['pct_whitenh']['indicator'])},\
    {'key': 'Black', 'val': '%4.1f%%' % (inds['pct_blacknh']['indicator'])},\
    {'key': 'Hispanic', 'val': '%4.1f%%' % (inds['pct_hispanic']['indicator'])},\
    {'key': 'Asian', 'val': '%4.1f%%' % (inds['pct_asiannh']['indicator'])},\
  ]
  proplist.append({'key': 'BR', 'val': ''})
  proplist.append({'key': 'Single-family', 'val': '%4.1f%%' % (inds['pct_sfh']['indicator'])})
  proplist.append({'key': 'Condo', 'val': '%4.1f%%' % (inds['pct_condo']['indicator'])})
  proplist.append({'key': 'Multi-family', 'val': '%4.1f%%' % (inds['pct_multifamily']['indicator'])})
  proplist.append({'key': 'Commercial/Industrial', 'val': '%4.1f%%' % (inds['pct_commind']['indicator'])})
  
  # And we're ready to render.
  return render_to_response('aggregate_geom.html', {\
    'title': search_geom_name,\
    'type': geom_type,\
    'proplist': proplist,\
    'mapcenter': mapcenter,\
    'outline': outline,\
    'histData': histData,\
    'timestreamData': timestreamData\
    },\
    context_instance=RequestContext(request))

def dajax_test(request):
  return render(request, 'landbank_data/dajax_test.html', {})

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

def leaflet(request):
    return render_to_response('landbank_data/leaflet.html')

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
  city_flag=True
  if geom_type=='Municipality' and search_geom_name!='Chicago': city_flag=False
  if geom_type=='Census Tract':
    city_geom=Municipality.objects.get(name='Chicago').geom
    if city_geom.intersection(search_geom.loc).area==0: city_flag=False
  # First get the community area.
  # Now get a bunch of indicator values for it.
  indicators = IndicatorCache.objects.\
    filter(area_type__exact=geom_type).\
    filter(area_id__exact=search_geom.id)

  # Basic info
  pop = int(indicators.get(indicator_name='pop').indicator_value)
  pct_white = indicators.get(indicator_name='pct_whitenh').indicator_value
  pct_black = indicators.get(indicator_name='pct_blacknh').indicator_value
  pct_asian = indicators.get(indicator_name='pct_asiannh').indicator_value
  pct_hispanic = indicators.get(indicator_name='pct_hispanic').indicator_value

  pct_sfh, pct_condo, pct_multifamily, pct_commind = None, None, None, None
  pct_sfh = indicators.get(indicator_name='pct_sfh').indicator_value
  pct_condo = indicators.get(indicator_name='pct_condo').indicator_value
  pct_multifamily = indicators.get(indicator_name='pct_multifamily').indicator_value
  pct_commind = indicators.get(indicator_name='pct_commind').indicator_value

  # Demographics
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
  pct_owner_occupieds_values, pct_owner_occupieds_bins, pct_owner_occupied_score = \
    indicator_hist(geom_type, 'pct_owner_occupied', pct_owner_occupied)
  pct_occ_units_values, pct_occ_units_bins, pct_occ_units_score = \
    indicator_hist(geom_type, 'pct_occ_units', pct_occ_units)
  segregations_values, segregations_bins, segregation_score = \
    indicator_hist(geom_type, 'segregation', segregation)
  owner_occ_hh_sizes_values, owner_occ_hh_sizes_bins, owner_occ_hh_size_score = \
    indicator_hist(geom_type, 'owner_occ_hh_size', owner_occ_hh_size)
  renter_occ_hh_sizes_values, renter_occ_hh_sizes_bins, renter_occ_hh_size_score = \
    indicator_hist(geom_type, 'renter_occ_hh_size', renter_occ_hh_size)
  median_ages_values, median_ages_bins, median_age_score = \
    indicator_hist(geom_type, 'median_age', median_age)
  demographics_hist_dicts = [\
    {'data': [{'x': b, 'y': v} for b,v in \
      zip(pct_owner_occupieds_bins,pct_owner_occupieds_values)],\
     'title': 'Owner occupancy rank: '+str(int(pct_owner_occupied_score)),\
     'label': 'Percent owner occupied', 'marker': pct_owner_occupied,\
     'tooltip': 'Percent owner occupied housing units'},
    {'data': [{'x': b, 'y': v} for b,v in \
      zip(pct_occ_units_bins,pct_occ_units_values)],\
     'title': 'Occupancy rank: '+str(int(pct_occ_units_score)),\
     'label': 'Percent occupied units', 'marker': pct_occ_units,\
     'tooltip': 'Percent housing units that are occupied'},\
    {'data': [{'x': b, 'y': v} for b,v in \
      zip(owner_occ_hh_sizes_bins,owner_occ_hh_sizes_values)],\
     'title': 'Owner crowding rank: '+str(int(owner_occ_hh_size_score)),\
     'label': 'Household size, owner-occupied', 'marker': owner_occ_hh_size,\
     'tooltip': 'Average household size in owner-occupied units'},\
    {'data': [{'x': b, 'y': v} for b,v in \
      zip(renter_occ_hh_sizes_bins,renter_occ_hh_sizes_values)],\
     'title': 'Renter crowding rank: '+str(int(renter_occ_hh_size_score)),\
     'label': 'Household size, renter-occupied', 'marker': renter_occ_hh_size,\
     'tooltip': 'Average household size in renter-occupied units'},\
    {'data': [{'x': b, 'y': v} for b,v in \
      zip(segregations_bins,segregations_values)],\
     'title': 'Segregation rank: '+str(int(segregation_score)),\
     'label': 'Segregation', 'marker': segregation,\
     'tooltip': 'Percentage of people who would have to move '+\
       'out for its racial and ethnic '+\
       'composition to match the city as a whole'},\
    {'data': [{'x': b, 'y': v} for b,v in \
      zip(median_ages_bins,median_ages_values)],\
     'title': 'Median age rank: '+str(int(median_age_score)),\
     'label': 'Median age', 'marker': median_age, \
     'tooltip': 'Median age of residents'}\
  ]

  # Economics
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
  jobs_within_mile_pc = indicators.get(indicator_name='jobs_within_mile_pc').\
    indicator_value
  jobs_within_mile_pc_values, jobs_within_mile_pc_bins, jobs_within_mile_pc_score = \
    indicator_hist(geom_type, 'jobs_within_mile_pc', jobs_within_mile_pc, hist_range=(0,5))
  if city_flag:
    construction_pc = indicators.get(indicator_name='construction_pc').\
      indicator_value
    construction_pc_values, construction_pc_bins, construction_pc_score = \
      indicator_hist(geom_type, 'construction_pc', construction_pc, hist_range=(0,5000))

  income_hist_dicts = [\
    {'title': 'Household income', 'label': 'Household income (thousands)', 'marker': med_inc,\
     'tooltip': 'Annual household income in thousands of dollars', 'data': inc_data},\
    {'title': 'Job access rank: '+str(int(jobs_within_mile_pc_score)),\
     'label': 'Jobs within 1 mile per capita', 'marker': jobs_within_mile_pc,\
     'tooltip': 'Jobs within 1 mile of this geometry, per capita', 'data': \
     [{'x': b, 'y': v} for b,v in zip(jobs_within_mile_pc_bins, jobs_within_mile_pc_values)]}]
  if city_flag:
    income_hist_dicts.append( 
    {'title': 'Construction rank: '+str(int(construction_pc_score)),\
     'label': 'Construction spending per capita', 'marker': construction_pc,\
     'tooltip': 'Spending on permitted construction per capita', 'data': \
     [{'x': b, 'y': v} for b,v in zip(construction_pc_bins, construction_pc_values)]})

  # Vacancy
  vacancy_usps = indicators.filter(indicator_name__exact='vacancy_usps').\
    latest('indicator_date').indicator_value
  vacancy_usps_values, vacancy_usps_bins, vacancy_usps_score = \
    indicator_hist(geom_type, 'vacancy_usps', vacancy_usps)
  if city_flag:
    demolitions_pc = indicators.filter(indicator_name__exact='demolitions_pc').\
      latest('indicator_date').indicator_value
    demolitions_pc_values, demolitions_pc_bins, demolitions_pc_score = \
      indicator_hist(geom_type, 'demolitions_pc', demolitions_pc)
    vacancy_311 = indicators.filter(indicator_name__exact='vacancy_311').\
      latest('indicator_date').indicator_value
    vacancy_311_values, vacancy_311_bins, vacancy_311_score = \
      indicator_hist(geom_type, 'vacancy_311', vacancy_311)

  vacancy_hist_dicts = [\
    {'title': 'USPS vacancy rank: '+str(int(vacancy_usps_score)),\
     'label': 'USPS vacancy rate', 'marker': vacancy_usps,\
     'tooltip': 'USPS percentage of vacant/no-stat residential addresses', 'data':\
     [{'x': b, 'y': v} for b,v in zip(vacancy_usps_bins, vacancy_usps_values)]}]
  if city_flag:
    vacancy_hist_dicts.append({\
     'title': 'Vacancy complaint rank: '+str(int(vacancy_311_score)),\
     'label': 'Vacancy complaint percentage', 'marker': vacancy_311,\
     'tooltip': 'Percentage of buildings with 311 vacant building complaints', 'data': \
     [{'x': b, 'y': v} for b,v in zip(vacancy_311_bins, vacancy_311_values)]})
    vacancy_hist_dicts.append({\
     'title': 'Demolition rank: '+str(int(demolitions_pc_score)),\
     'label': 'Demolition permits per 1000', 'marker': demolitions_pc*1000,\
     'tooltip': 'Demolition permits per 1000 residents', 'data': \
     [{'x': b*1000, 'y': v} for b,v in zip(demolitions_pc_bins, demolitions_pc_values)]})

  

  # Market
  foreclosure_rate = indicators.filter(indicator_name__exact='foreclosure_rate').\
    latest('indicator_date').indicator_value
  foreclosure_rates_values, foreclosure_rates_bins, foreclosure_score = \
    indicator_hist(geom_type, 'foreclosure_rate',foreclosure_rate)
  median_price = indicators.filter(indicator_name__exact='median_price').\
    latest('indicator_date').indicator_value
  median_prices_values, median_prices_bins, price_score = \
    indicator_hist(geom_type, 'median_price',median_price)
  transactions_per_thousand = indicators.filter(indicator_name__exact='transactions_per_thousand').\
    latest('indicator_date').indicator_value
  transactions_per_thousands_values, transactions_per_thousands_bins, velocity_score = \
    indicator_hist(geom_type, 'transactions_per_thousand', transactions_per_thousand, hist_range=(0,25))
  mortgages_per_thousand = indicators.filter(indicator_name__exact='mortgages_per_thousand').\
    latest('indicator_date').indicator_value
  mortgages_per_thousands_values, mortgages_per_thousands_bins, mortgage_score = \
    indicator_hist(geom_type, 'mortgages_per_thousand', mortgages_per_thousand, hist_range=(0,100))
  percent_lowvalue = indicators.filter(indicator_name__exact='percent_lowvalue').\
    latest('indicator_date').indicator_value
  percent_lowvalues_values, percent_lowvalues_bins, lowvalue_score = \
    indicator_hist(geom_type, 'percent_lowvalue', percent_lowvalue)
  percent_businessbuyer = indicators.filter(indicator_name__exact='percent_businessbuyers').\
    latest('indicator_date').indicator_value
  percent_businessbuyers_values, percent_businessbuyers_bins, spec_score = \
    indicator_hist(geom_type, 'percent_businessbuyers',percent_businessbuyer)
  market_hist_dicts = [\
    {'title': 'Foreclosure rank: '+str(foreclosure_score),\
     'label': 'Foreclosure rate', 'marker': foreclosure_rate,\
     'tooltip': 'Foreclosures per thousand residential properties (single-family and condo, prev. quarter)',\
     'data': [{'x': b, 'y': v} for b,v in \
     zip(foreclosure_rates_bins, foreclosure_rates_values)]},\
    {'title': 'Price rank: '+str(price_score),\
     'label': 'Median price', 'marker': median_price,\
     'tooltip': 'Median price for residential properties (single-family and condo, prev. quarter)',\
     'data': [{'x': b, 'y': v} for b,v in \
     zip(median_prices_bins, median_prices_values)]},\
    {'title': 'Velocity rank: '+str(velocity_score),\
     'label': 'Transactions per thousand', 'marker': transactions_per_thousand,\
     'tooltip': 'Transactions per thousand residential properties (single-family and condo, prev. quarter)',\
     'data': [{'x': b, 'y': v} for b,v in \
     zip(transactions_per_thousands_bins, transactions_per_thousands_values)]},\
    {'title': 'Credit availability rank: '+str(mortgage_score),\
     'label': 'Mortgages per thousand', 'marker': mortgages_per_thousand,\
     'tooltip': 'Mortgages per thousand residential properties (single-family and condo, prev. quarter)',\
     'data': [{'x': b, 'y': v} for b,v in \
     zip(mortgages_per_thousands_bins, mortgages_per_thousands_values)]},\
    {'title': 'Low-value rank: '+str(lowvalue_score),\
     'label': 'Percent low-value transactions', 'marker': percent_lowvalue,\
     'tooltip': 'Percent residential transactions for <$20k (single-family and condo, prev. quarter)',\
     'data': [{'x': b, 'y': v} for b,v in \
     zip(percent_lowvalues_bins, percent_lowvalues_values)]},\
    {'title': 'Speculation rank: '+str(spec_score),\
     'label': 'Percent business buyers', 'marker': percent_businessbuyer,\
     'tooltip': 'Percent business buyers (single-family and condo, prev. quarter)',\
     'data': [{'x': b, 'y': v} for b,v in \
     zip(percent_businessbuyers_bins, percent_businessbuyers_values)]}\
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
    {('Income','First black line marks median household income of this tract, remainder mark this '+\
    geom_type+' relative to all others') : income_hist_dicts },\
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
    {'key': 'Population', 'val': pop},\
    {'key': 'BR', 'val': ''},\
    {'key': 'White', 'val': '%4.1f%%' % (pct_white)},\
    {'key': 'Black', 'val': '%4.1f%%' % (pct_black)},\
    {'key': 'Hispanic', 'val': '%4.1f%%' % (pct_hispanic)},\
    {'key': 'Asian', 'val': '%4.1f%%' % (pct_asian)},\
  ]
  proplist.append({'key': 'BR', 'val': ''})
  proplist.append({'key': 'Single-family', 'val': '%4.1f%%' % (pct_sfh)})
  proplist.append({'key': 'Condo', 'val': '%4.1f%%' % (pct_condo)})
  proplist.append({'key': 'Multi-family', 'val': '%4.1f%%' % (pct_multifamily)})
  proplist.append({'key': 'Commercial/Industrial', 'val': '%4.1f%%' % (pct_commind)})
  
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

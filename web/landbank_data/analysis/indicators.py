from models import \
  CommunityArea, Ward, CensusTract, Municipality, \
  CensusTractMapping, AreaPlotCache, CensusTractCharacteristics, \
  IndicatorCache, Transaction, Foreclosure, Mortgage, Assessor
import json, datetime
import numpy as np
from indicator_utils import *
from pytz import timezone

cst=timezone('US/Central')

def cache_population():
  # Total population.
  for geom_type,geom_str in \
    zip([CensusTract,Municipality,Ward,CommunityArea],\
        ['Census Tract', 'Municipality', 'Ward', 'Community Area']):
    for geom in geom_type.objects.all():
      cv = IndicatorCache(\
        area_type=geom_str, area_id = geom.id,\
        indicator_name = 'pop',\
        indicator_value = get_population(geoms=geom))
      cv.save()

def cache_census():
  # Other census indicators.
  for indicator in ['median_age', 'pct_18plus', 'pct_65plus', 'pct_whitenh',\
                    'pct_blacknh', 'pct_asiannh', 'pct_hispanic', 'pct_owner_occupied',\
                    'pct_occ_units',\
                    'pct_renter_occupied', 'owner_occ_hh_size', 'renter_occ_hh_size']:

    for geom_type,geom_str in \
      zip([CensusTract,Municipality,Ward,CommunityArea],\
          ['Census Tract', 'Municipality', 'Ward', 'Community Area']):
      for geom in geom_type.objects.all():
        retval = get_pop_weighted_characteristic(indicator, geoms=geom)
        cv = IndicatorCache(\
          area_type=geom_str,\
          area_id  = geom.id,\
          indicator_name  = indicator,\
          indicator_value = retval)
        cv.save()


def cache_segregation():
  # Segregation index
  tot_pct_white = get_pop_weighted_characteristic("pct_whitenh",\
    tracts=CensusTract.objects.all())
  tot_pct_black = get_pop_weighted_characteristic("pct_blacknh",\
    tracts=CensusTract.objects.all())
  tot_pct_hisp = get_pop_weighted_characteristic("pct_hispanic",\
    tracts=CensusTract.objects.all())
  tot_pct_asian = get_pop_weighted_characteristic("pct_asiannh",\
    tracts=CensusTract.objects.all())

  # We'll define it as the percentage of people who would have to
  # move in order for the geometry to match Cook County as a whole.
  for geom_type,geom_str in \
    zip([CensusTract,Municipality,Ward,CommunityArea],\
        ['Census Tract', 'Municipality', 'Ward', 'Community Area']):
    for geom in geom_type.objects.all():
      pct_white = get_pop_weighted_characteristic("pct_whitenh",\
        geoms=geom)
      pct_black = get_pop_weighted_characteristic("pct_blacknh",\
        geoms=geom)
      pct_hisp = get_pop_weighted_characteristic("pct_hispanic",\
        geoms=geom)
      pct_asian = get_pop_weighted_characteristic("pct_asiannh",\
        geoms=geom)
      segregation = (\
        abs(tot_pct_white-pct_white)+\
        abs(tot_pct_black-pct_black)+\
        abs(tot_pct_hisp-pct_hisp)+\
        abs(tot_pct_asian-pct_asian))/2.0
      cv = IndicatorCache(\
        area_type=geom_str, area_id = geom.id,\
        indicator_name = 'segregation',\
        indicator_value = segregation)
      cv.save()

def quarter_to_datetime(quarter):
  quarter=str(quarter)
  thisyear=quarter[:4]
  thismonth='10'
  if   quarter[4]=='1': thismonth='1'
  elif quarter[4]=='2': thismonth='4'
  elif quarter[4]=='3': thismonth='7'
  return cst.localize(datetime.datetime.strptime(thisyear+'/'+thismonth, '%Y/%m'))

def cache_market_indicators():
  for geom_type,geom_str in \
    zip([CensusTract,Municipality,Ward,CommunityArea],\
        ['Census Tract', 'Municipality', 'Ward', 'Community Area']):
    for geom in geom_type.objects.all():
      print '.'
      retval = get_foreclosure_rate(geoms=geom)
      for k,v in retval.iteritems():
        cv = IndicatorCache(\
          area_type=geom_str, area_id = geom.id,\
          indicator_name='foreclosure_rate',\
          indicator_value = v,\
          indicator_date = quarter_to_datetime(k))
        cv.save()
      retval = get_median_price(geoms=geom)
      for k,v in retval.iteritems():
        cv = IndicatorCache(\
          area_type=geom_str, area_id = geom.id,\
          indicator_name='median_price',\
          indicator_value = v,\
          indicator_date = quarter_to_datetime(k))
        cv.save()
      retval = get_transactions_per_thousand(geoms=geom)
      for k,v in retval.iteritems():
        cv = IndicatorCache(\
          area_type=geom_str, area_id = geom.id,\
          indicator_name='transactions_per_thousand',\
          indicator_value = v,\
          indicator_date = quarter_to_datetime(k))
        cv.save()
      retval = get_mortgages_per_thousand(geoms=geom)
      for k,v in retval.iteritems():
        cv = IndicatorCache(\
          area_type=geom_str, area_id = geom.id,\
          indicator_name='mortgages_per_thousand',\
          indicator_value = v,\
          indicator_date = quarter_to_datetime(k))
        cv.save()
      retval = get_percent_lowvalue_transactions(geoms=geom)
      for k,v in retval.iteritems():
        cv = IndicatorCache(\
          area_type=geom_str, area_id = geom.id,\
          indicator_name='percent_lowvalue',\
          indicator_value = v,\
          indicator_date = quarter_to_datetime(k))
        cv.save()
      retval = get_percent_business_buyers(geoms=geom)
      for k,v in retval.iteritems():
        cv = IndicatorCache(\
          area_type=geom_str, area_id = geom.id,\
          indicator_name='percent_businessbuyers',\
          indicator_value = v,\
          indicator_date = quarter_to_datetime(k))
        cv.save()

def get_foreclosure_rate(\
  tracts=None, communityareas=None,\
  municipalities=None, wards=None, geoms=None):
  # Example usage:
  # indicators.get_foreclosure_rate(geoms=CensusTract.objects.filter(fips__in=(17031840300, 17031840200)))
  if geoms is not None:
    tracts, wards, communityareas, municipalities = unpack_geoms(geoms,\
      tracts=tracts, communityareas=communityareas, municipalities=municipalities,\
      wards=wards)
  geoms = unite_geoms(\
      tracts=tracts, communityareas=communityareas, municipalities=municipalities,\
      wards=wards)
  assess = Assessor.objects.filter(loc__contained=geoms).\
    filter(loc__contained=geoms).\
    filter(ptype_id__in=[1,2])
  retval = {}
  for yq in Foreclosure.objects.distinct('adj_yq'):
    forecs = Foreclosure.objects.\
      filter(loc__contained=geoms).\
      filter(ptype_id__in=[1,2]).\
      filter(adj_yq__exact=yq.adj_yq)
    if len(assess) == 0:
      retval[yq.adj_yq] = 0
    else:
      retval[yq.adj_yq] = float(len(forecs))/len(assess)*1000
  return retval

def get_median_price(\
  tracts=None, communityareas=None,\
  municipalities=None, wards=None, geoms=None):
  # Example usage:
  # indicators.get_median_price(geoms=CensusTract.objects.filter(fips__in=(17031840300, 17031840200)))
  if geoms is not None:
    tracts, wards, communityareas, municipalities = unpack_geoms(geoms,\
      tracts=tracts, communityareas=communityareas, municipalities=municipalities,\
      wards=wards)
  geoms = unite_geoms(\
      tracts=tracts, communityareas=communityareas, municipalities=municipalities,\
      wards=wards)
  retval = {}
  for yq in Transaction.objects.distinct('adj_yq'):
    transact = Transaction.objects.\
      filter(loc__contained=geoms).\
      filter(ptype_id__in=[1,2]).\
      filter(adj_yq__exact=yq.adj_yq)
    if len(transact) == 0:
      retval[yq.adj_yq] = 0
    else:
      retval[yq.adj_yq] = np.median([i.amount_prime for i in transact])
  return retval

def get_percent_business_buyers(\
  tracts=None, communityareas=None,\
  municipalities=None, wards=None, geoms=None):
  # Example usage:
  # indicators.get_median_price(geoms=CensusTract.objects.filter(fips__in=(17031840300, 17031840200)))
  if geoms is not None:
    tracts, wards, communityareas, municipalities = unpack_geoms(geoms,\
      tracts=tracts, communityareas=communityareas, municipalities=municipalities,\
      wards=wards)
  geoms = unite_geoms(\
      tracts=tracts, communityareas=communityareas, municipalities=municipalities,\
      wards=wards)
  retval = {}
  for yq in Transaction.objects.distinct('adj_yq'):
    transact = Transaction.objects.\
      filter(loc__contained=geoms).\
      filter(ptype_id__in=[1,2]).\
      filter(adj_yq__exact=yq.adj_yq)
    busbuyer = Transaction.objects.\
      filter(loc__contained=geoms).\
      filter(business_buyer__exact=1).\
      filter(ptype_id__in=[1,2]).\
      filter(adj_yq__exact=yq.adj_yq)
    if len(transact) == 0:
      retval[yq.adj_yq] = 0
    else:
      retval[yq.adj_yq] = len(busbuyer)/float(len(transact))*100
  return retval


def get_percent_lowvalue_transactions(\
  tracts=None, communityareas=None,\
  municipalities=None, wards=None, geoms=None):
  # Example usage:
  # indicators.get_median_price(geoms=CensusTract.objects.filter(fips__in=(17031840300, 17031840200)))
  if geoms is not None:
    tracts, wards, communityareas, municipalities = unpack_geoms(geoms,\
      tracts=tracts, communityareas=communityareas, municipalities=municipalities,\
      wards=wards)
  geoms = unite_geoms(\
      tracts=tracts, communityareas=communityareas, municipalities=municipalities,\
      wards=wards)
  retval = {}
  for yq in Transaction.objects.distinct('adj_yq'):
    transact = Transaction.objects.\
      filter(loc__contained=geoms).\
      filter(ptype_id__in=[1,2]).\
      filter(adj_yq__exact=yq.adj_yq)
    lowvalue = Transaction.objects.\
      filter(loc__contained=geoms).\
      filter(purchase_less_20k__exact=1).\
      filter(ptype_id__in=[1,2]).\
      filter(adj_yq__exact=yq.adj_yq)
    if len(transact) == 0:
      retval[yq.adj_yq] = 0
    else:
      retval[yq.adj_yq] = len(lowvalue)/float(len(transact))*100
  return retval


def get_transactions_per_thousand(\
  tracts=None, communityareas=None,\
  municipalities=None, wards=None, geoms=None):
  # Example usage:
  # indicators.get_median_price(geoms=CensusTract.objects.filter(fips__in=(17031840300, 17031840200)))
  if geoms is not None:
    tracts, wards, communityareas, municipalities = unpack_geoms(geoms,\
      tracts=tracts, communityareas=communityareas, municipalities=municipalities,\
      wards=wards)
  geoms = unite_geoms(\
      tracts=tracts, communityareas=communityareas, municipalities=municipalities,\
      wards=wards)
  retval = {}
  pop = get_population(\
      tracts=tracts, communityareas=communityareas, municipalities=municipalities,\
      wards=wards)
  for yq in Transaction.objects.distinct('adj_yq'):
    transact = Transaction.objects.\
      filter(loc__contained=geoms).\
      filter(ptype_id__in=[1,2]).\
      filter(adj_yq__exact=yq.adj_yq)
    if pop == 0:
      retval[yq.adj_yq] = 0
    else:
      retval[yq.adj_yq] = len([i.amount_prime for i in transact])/float(pop)*1000
  return retval


def get_mortgages_per_thousand(\
  tracts=None, communityareas=None,\
  municipalities=None, wards=None, geoms=None):
  if geoms is not None:
    tracts, wards, communityareas, municipalities = unpack_geoms(geoms,\
      tracts=tracts, communityareas=communityareas, municipalities=municipalities,\
      wards=wards)
  geoms = unite_geoms(\
      tracts=tracts, communityareas=communityareas, municipalities=municipalities,\
      wards=wards)
  pop = get_population(\
      tracts=tracts, communityareas=communityareas, municipalities=municipalities,\
      wards=wards)
  retval = {}
  for yq in Mortgage.objects.distinct('adj_yq'):
    mortgages = Mortgage.objects.\
      filter(loc__contained=geoms).\
      filter(ptype_id__in=[1,2]).\
      filter(adj_yq__exact=yq.adj_yq)
    if pop == 0:
      retval[yq.adj_yq] = 0
    else:
      retval[yq.adj_yq] = len(mortgages)/float(pop)*1000
  return retval

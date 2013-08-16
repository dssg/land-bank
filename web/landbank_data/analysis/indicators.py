from models import \
  CommunityArea, Ward, CensusTract, Municipality, \
  CensusTractMapping, AreaPlotCache, CensusTractCharacteristics, \
  IndicatorCache, Transaction, Foreclosure, Mortgage, Assessor,\
  CensusBlock, CensusBlockEmployment, VacancyUSPS, Vacancy311,\
  BuildingPermit
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

def cache_income():
  for field in [\
    'inc_lt_10', 'inc_10_15', 'inc_15_25', 'inc_25_35',\
    'inc_35_50', 'inc_50_75', 'inc_75_100', 'inc_100_150',\
    'inc_150_200', 'inc_gt_200', 'med_inc']:
    for geom_type,geom_str in \
      zip([CensusTract,Municipality,Ward,CommunityArea],\
          ['Census Tract', 'Municipality', 'Ward', 'Community Area']):
      for geom in geom_type.objects.all():
        val = get_pop_weighted_characteristic(field,\
        geoms=geom, income=True)
        cv = IndicatorCache(\
          area_type=geom_str, area_id = geom.id,\
          indicator_name = field,\
          indicator_value = val)
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

def get_jobs_within_dist(dist,\
  tracts=None, communityareas=None,\
  municipalities=None, wards=None, geoms=None):
  if geoms is not None:
    tracts, wards, communityareas, municipalities = unpack_geoms(geoms,\
      tracts=tracts, communityareas=communityareas, municipalities=municipalities,\
      wards=wards)
  geoms = unite_geoms(\
      tracts=tracts, communityareas=communityareas, municipalities=municipalities,\
      wards=wards)
  blockswithin = CensusBlock.objects.filter(loc__dwithin=(geoms,dist))
  retval = 0
  for block in blockswithin:
    retval += sum([i.jobs for i in block.censusblockemployment_set.all()])
  return retval

def get_vacancyusps(\
  tracts=None, communityareas=None,\
  municipalities=None, wards=None, geoms=None):
  if geoms is not None:
    tracts, wards, communityareas, municipalities = unpack_geoms(geoms,\
      tracts=tracts, communityareas=communityareas, municipalities=municipalities,\
      wards=wards)
  retval = {}
  for y, q in [(i.year, i.quarter) for i in VacancyUSPS.objects.distinct('year','quarter')]:
    num, den = 0.0, 0.0
    if tracts is not None:
     for tract in iterable(tracts): 
      try:
       v = VacancyUSPS.objects.get(fips=tract.fips, year=y, quarter=q)
       num += v.res_vacant + v.res_nostat
       den += v.naddr_res
      except: continue
    if municipalities is not None:
     for muni in iterable(municipalities):
      for tract_mapping in muni.censustractmapping_set.all():
       try:
        v = VacancyUSPS.objects.get(fips=tract_mapping.fips, year=y, quarter=q)
        num += (v.res_vacant + v.res_nostat) * tract_mapping.municipality_frac
        den += (v.naddr_res) * tract_mapping.municipality_frac
       except: continue
    if wards is not None:
     for ward in iterable(wards):
      for tract_mapping in ward.censustractmapping_set.all():
       try:
        v = VacancyUSPS.objects.get(fips=tract_mapping.fips, year=y, quarter=q)
        num += (v.res_vacant + v.res_nostat) * tract_mapping.ward_frac
        den += (v.naddr_res) * tract_mapping.ward_frac
       except: continue
    if communityareas is not None:
     for communityarea in iterable(communityareas):
      for tract_mapping in communityarea.censustractmapping_set.all():
       try:
        v = VacancyUSPS.objects.get(fips=tract_mapping.fips, year=y, quarter=q)
        num += (v.res_vacant + v.res_nostat) * tract_mapping.communityarea_frac
        den += (v.naddr_res) * tract_mapping.communityarea_frac
       except: continue
    retval[int(str(y)+str(q))] = float(num)/den*100 if den!=0 else 0
  return retval
   
def cache_vacancy_indicators():
  cache_demolition_indicator()
  cache_vacancyusps_indicator()
  cache_vacancy311_indicator()

def cache_vacancyusps_indicator():
  for geom_type,geom_str in \
    zip([CensusTract,Municipality,Ward,CommunityArea],\
        ['Census Tract', 'Municipality', 'Ward', 'Community Area']):
    for geom in geom_type.objects.all():
      print '.'
      retval = get_vacancyusps(geoms=geom)
      for k,v in retval.iteritems():
        cv = IndicatorCache(\
          area_type=geom_str, area_id = geom.id,\
          indicator_name='vacancy_usps',\
          indicator_value = v*100.0,\
          indicator_date = quarter_to_datetime(k))
        cv.save()

def cache_vacancy311_indicator():
  lastyear = cst.localize(datetime.datetime.now() - datetime.timedelta(days=365.25))
  city_geom=Municipality.objects.get(name='Chicago').geom
  for geom_type,geom_str in \
    zip([CensusTract,Municipality,Ward,CommunityArea],\
        ['Census Tract', 'Municipality', 'Ward', 'Community Area']):
    for geom in geom_type.objects.all():
      if (geom_type==CensusTract):
        if not city_geom.intersects(geom.loc): continue
        myinds = Vacancy311.objects.filter(loc__within=geom.loc).\
                            filter(request_date__gte=lastyear)
        assess = Assessor.objects.filter(loc__contained=geom.loc)
        cv = IndicatorCache(\
          area_type=geom_str, area_id = geom.id,\
          indicator_name='vacancy_311',\
          indicator_value = float(len(myinds))/len(assess)*100,\
          indicator_date = lastyear)
        cv.save()
      else:
        if not city_geom.intersects(geom.geom): continue
        if geom_type==Municipality and geom.name!='Chicago': continue
        myinds = Vacancy311.objects.filter(loc__within=geom.geom).\
                            filter(request_date__gte=lastyear)
        assess = Assessor.objects.filter(loc__contained=geom.geom)
        cv = IndicatorCache(\
          area_type=geom_str, area_id = geom.id,\
          indicator_name='vacancy_311',\
          indicator_value = float(len(myinds))/len(assess)*100,\
          indicator_date = lastyear)
        cv.save()

def cache_accessibility_indicators():
  for geom_type,geom_str in \
    zip([CensusTract,Municipality,Ward,CommunityArea],\
        ['Census Tract', 'Municipality', 'Ward', 'Community Area']):
    for geom in geom_type.objects.all():
      geomloc = geom.loc if geom_type==CensusTract else geom.geom
      blocks = CensusBlock.objects.filter(loc__dwithin=(geomloc, 5280))
      retval = 0.0
      for block in blocks:
        for emp in block.censusblockemployment_set.all(): retval += emp.jobs
      pop = IndicatorCache.objects.get(indicator_name='pop', \
            area_type=geom_str, area_id=geom.id).indicator_value
      if pop==0: continue
      cv = IndicatorCache(\
        area_type=geom_str, area_id = geom.id,\
        indicator_name='jobs_within_mile_pc',\
        indicator_value = retval/float(pop))
      cv.save()

def cache_demolition_indicator():
  lastyear = cst.localize(datetime.datetime.now() - datetime.timedelta(days=365.25))
  city_geom=Municipality.objects.get(name='Chicago').geom
  for geom_type,geom_str in \
    zip([CensusTract,Municipality,Ward,CommunityArea],\
        ['Census Tract', 'Municipality', 'Ward', 'Community Area']):
    for geom in geom_type.objects.all():
      pop = IndicatorCache.objects.get(indicator_name='pop', \
            area_type=geom_str, area_id=geom.id).indicator_value
      if pop==0: continue
      if (geom_type==CensusTract):
        if not city_geom.intersects(geom.loc): continue
        myinds = BuildingPermit.objects.filter(loc__within=geom.loc).\
                            filter(timestamp__gte=lastyear).\
                            filter(permit_type__exact='PERMIT - WRECKING/DEMOLITION')
        cv = IndicatorCache(\
          area_type=geom_str, area_id = geom.id,\
          indicator_name='demolitions_pc',\
          indicator_value = float(len(myinds))/pop,\
          indicator_date = lastyear)
        cv.save()
      else:
        if not city_geom.intersects(geom.geom): continue
        if geom_type==Municipality and geom.name!='Chicago': continue
        myinds = BuildingPermit.objects.filter(loc__within=geom.geom).\
                            filter(timestamp__gte=lastyear).\
                            filter(permit_type__exact='PERMIT - WRECKING/DEMOLITION')
        cv = IndicatorCache(\
          area_type=geom_str, area_id = geom.id,\
          indicator_name='demolitions_pc',\
          indicator_value = float(len(myinds))/pop,\
          indicator_date = lastyear)
        cv.save()

def cache_construction_indicator():
  lastyear = cst.localize(datetime.datetime.now() - datetime.timedelta(days=365.25))
  city_geom=Municipality.objects.get(name='Chicago').geom
  for geom_type,geom_str in \
    zip([CensusTract,Municipality,Ward,CommunityArea],\
        ['Census Tract', 'Municipality', 'Ward', 'Community Area']):
    for geom in geom_type.objects.all():
      pop = IndicatorCache.objects.get(indicator_name='pop', \
            area_type=geom_str, area_id=geom.id).indicator_value
      if pop==0: continue
      if (geom_type==CensusTract):
        if not city_geom.intersects(geom.loc): continue
        myinds = BuildingPermit.objects.filter(loc__within=geom.loc).\
                            filter(timestamp__gte=lastyear)
        retval = 0
        for myind in myinds: 
          if myind.cost is not None: retval += myind.cost
        cv = IndicatorCache(\
          area_type=geom_str, area_id = geom.id,\
          indicator_name='construction_pc',\
          indicator_value = float(retval)/pop,\
          indicator_date = lastyear)
        cv.save()
      else:
        if not city_geom.intersects(geom.geom): continue
        if geom_type==Municipality and geom.name!='Chicago': continue
        myinds = BuildingPermit.objects.filter(loc__within=geom.geom).\
                            filter(timestamp__gte=lastyear)
        retval = 0
        for myind in myinds: 
          if myind.cost is not None: retval += myind.cost
        cv = IndicatorCache(\
          area_type=geom_str, area_id = geom.id,\
          indicator_name='construction_pc',\
          indicator_value = float(retval)/pop,\
          indicator_date = lastyear)
        cv.save()

def cache_landuse_indicators():
  city_geom=Municipality.objects.get(name='Chicago').geom
  for geom_type,geom_str in \
    zip([CensusTract,Municipality,Ward,CommunityArea],\
        ['Census Tract', 'Municipality', 'Ward', 'Community Area']):
    for geom in geom_type.objects.all():
      allpins, sfh, condo, multi, commind = None, None, None, None, None
      if (geom_type==CensusTract):
        if not city_geom.intersects(geom.loc): continue
        allpins = Assessor.objects.filter(loc__within=geom.loc)
        sfh     = Assessor.objects.filter(loc__within=geom.loc).\
                                   filter(ptype_id__exact=1)
        condo   = Assessor.objects.filter(loc__within=geom.loc).\
                                   filter(ptype_id__exact=2)
        multi   = Assessor.objects.filter(loc__within=geom.loc).\
                                   filter(ptype_id__in=(3,4))
        commind = Assessor.objects.filter(loc__within=geom.loc).\
                                   filter(ptype_id__exact=(5))
      else:
        if not city_geom.intersects(geom.geom): continue
        if geom_type==Municipality and geom.name!='Chicago': continue
        allpins = Assessor.objects.filter(loc__within=geom.geom)
        sfh     = Assessor.objects.filter(loc__within=geom.geom).\
                                   filter(ptype_id__exact=1)
        condo   = Assessor.objects.filter(loc__within=geom.geom).\
                                   filter(ptype_id__exact=2)
        multi   = Assessor.objects.filter(loc__within=geom.geom).\
                                   filter(ptype_id__in=(3,4))
        commind = Assessor.objects.filter(loc__within=geom.geom).\
                                   filter(ptype_id__exact=(5))
      tot_pins = len(allpins)
      if tot_pins == 0: continue
      cv = IndicatorCache(\
        area_type=geom_str, area_id = geom.id,\
        indicator_name='pct_sfh',\
        indicator_value = float(len(sfh))/len(allpins)*100)
      cv.save()
      cv = IndicatorCache(\
        area_type=geom_str, area_id = geom.id,\
        indicator_name='pct_condo',\
        indicator_value = float(len(condo))/len(allpins)*100)
      cv.save()
      cv = IndicatorCache(\
        area_type=geom_str, area_id = geom.id,\
        indicator_name='pct_multifamily',\
        indicator_value = float(len(multi))/len(allpins)*100)
      cv.save()
      cv = IndicatorCache(\
        area_type=geom_str, area_id = geom.id,\
        indicator_name='pct_commind',\
        indicator_value = float(len(commind))/len(allpins)*100)
      cv.save()


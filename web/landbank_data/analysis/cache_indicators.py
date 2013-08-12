from models import \
  CommunityArea, Ward, CensusTract, Municipality, \
  CensusTractMapping, AreaPlotCache, CensusTractCharacteristics, \
  IndicatorCache
import json
import numpy as np

def iterable(obj):
  try:    iter(obj)
  except: return [obj]
  return obj

def get_tract_characteristic(characteristic, tracts):
  retval = {}
  for tract in iterable(tracts):
    tc = CensusTractCharacteristics.objects.get(\
      fips=tract.fips)
    retval[tract] = getattr(tc,characteristic)
    if retval[tract] is None: retval[tract]=0.0
  return retval

def get_tract_from_fips(fips):
  return CensusTract.objects.get(fips__exact=fips)

def get_tracts_and_weights(\
  tracts=None, communityareas=None,\
  municipalities=None, wards=None):
  retval = {}
  if tracts is not None:
    for tract in iterable(tracts):
      retval[tract]=1.0
  if communityareas is not None:
    for ca in iterable(communityareas):
      t = ca.censustractmapping_set.all()
      for i in t: 
        thistract = get_tract_from_fips(i.fips)
        if thistract not in retval.keys(): retval[thistract]=i.communityarea_frac
        else: retval[thistract] = max(i.communityarea_frac, retval[thistract])
  if municipalities is not None:
    for m in iterable(municipalities):
      t = m.censustractmapping_set.all()
      for i in t: 
        thistract = get_tract_from_fips(i.fips)
        if thistract not in retval.keys(): retval[thistract]=i.municipality_frac
        else: retval[thistract] = max(i.municipality_frac, retval[thistract])
  if wards is not None:
    for w in iterable(wards):
      t = w.censustractmapping_set.all()
      for i in t: 
        thistract = get_tract_from_fips(i.fips)
        if thistract not in retval.keys(): retval[thistract]=i.ward_frac
        else: retval[thistract] = max(i.ward_frac, retval[thistract])
  return retval
  
def get_population(
  tracts=None, communityareas=None,\
  municipalities=None, wards=None):
  tracts = get_tracts_and_weights(tracts,communityareas,municipalities,wards)
  pops = get_tract_characteristic('pop',tracts.keys())
  return int(sum([pops[i]*tracts[i] for i in pops.keys()]))

def get_pop_weighted_characteristic(characteristic,
  tracts=None, communityareas=None,\
  municipalities=None, wards=None):
  tracts = get_tracts_and_weights(tracts,communityareas,municipalities,wards)
  pops = get_tract_characteristic('pop',tracts.keys())
  vals = get_tract_characteristic(characteristic,tracts.keys())
  norm = sum([pops[i]*tracts[i] for i in pops.keys()])
  return sum([pops[i]*tracts[i]*vals[i] for i in pops.keys()])/norm \
    if norm > 0 else 0

def cache_census_indicators():
  for tract in CensusTract.objects.all():
    cv = IndicatorCache(\
      area_type='Census Tract', area_id = tract.id,\
      indicator_name = 'pop',\
      indicator_value = get_population(tracts=tract))
    cv.save()
  for municipality in Municipality.objects.all():
    cv = IndicatorCache(\
      area_type='Municipality', area_id = municipality.id,\
      indicator_name = 'pop',\
      indicator_value = get_population(municipalities=municipality))
    cv.save()
  for communityarea in CommunityArea.objects.all():
    cv = IndicatorCache(\
      area_type='Community Area', area_id = communityarea.id,\
      indicator_name = 'pop',\
      indicator_value = get_population(communityareas=communityarea))
    cv.save()
  for ward in Ward.objects.all():
    cv = IndicatorCache(\
      area_type='Ward', area_id = ward.id,\
      indicator_name = 'pop',\
      indicator_value = get_population(wards=ward))
    cv.save()

  for indicator in ['median_age', 'pct_18plus', 'pct_65plus', 'pct_whitenh',\
                    'pct_blacknh', 'pct_asiannh', 'pct_hispanic', 'pct_owner_occupied',\
                    'pct_renter_occupied', 'owner_occ_hh_size', 'renter_occ_hh_size']:

    for tract in CensusTract.objects.all():
      retval = get_pop_weighted_characteristic(indicator,\
        tracts=tract)
      cv = IndicatorCache(\
        area_type='Census Tract',\
        area_id  = tract.id,\
        indicator_name  = indicator,\
        indicator_value = retval)
      cv.save()

    for municipality in Municipality.objects.all():
      retval = get_pop_weighted_characteristic(indicator,\
        municipalities=municipality)
      cv = IndicatorCache(\
        area_type='Municipality',\
        area_id  = municipality.id,\
        indicator_name  = indicator,\
        indicator_value = retval)
      cv.save()

    for communityarea in CommunityArea.objects.all():
      retval = get_pop_weighted_characteristic(indicator,\
        communityareas=communityarea)
      cv = IndicatorCache(\
        area_type='Community Area',\
        area_id  = communityarea.id,\
        indicator_name  = indicator,\
        indicator_value = retval)
      cv.save()

    for ward in Ward.objects.all():
      retval = get_pop_weighted_characteristic(indicator,\
        wards=ward)
      cv = IndicatorCache(\
        area_type='Ward',\
        area_id  = ward.id,\
        indicator_name  = indicator,\
        indicator_value = retval)
      cv.save()

def cache_indicators():
  IndicatorCache.objects.all().delete()
  cache_census_indicators()
      

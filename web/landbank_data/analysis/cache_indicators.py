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
  municipalities=None, wards=None, geoms=None):
  if geoms is not None:
    for g in iterable(geoms):
      if isinstance(g,CensusTract):
        if tracts==None: tracts=[g]
        else: tracts.append(g)
      if isinstance(g,Ward):
        if wards==None: wards=[g]
        else: wards.append(g)
      if isinstance(g,CommunityArea):
        if communityareas==None: communityareas=[g]
        else: communityareas.append(g)
      if isinstance(g,Municipality):
        if municipalities==None: municipalities=[g]
        else: municipalities.append(g)
  tracts = get_tracts_and_weights(tracts,communityareas,municipalities,wards)
  pops = get_tract_characteristic('pop',tracts.keys())
  vals = get_tract_characteristic(characteristic,tracts.keys())
  tracts = get_tracts_and_weights(tracts,communityareas,municipalities,wards)
  pops = get_tract_characteristic('pop',tracts.keys())
  return int(sum([pops[i]*tracts[i] for i in pops.keys()]))

def get_pop_weighted_characteristic(characteristic,
  tracts=None, communityareas=None,\
  municipalities=None, wards=None, geoms=None):
  if geoms is not None:
    for g in iterable(geoms):
      if isinstance(g,CensusTract):
        if tracts==None: tracts=[g]
        else: tracts.append(g)
      if isinstance(g,Ward):
        if wards==None: wards=[g]
        else: wards.append(g)
      if isinstance(g,CommunityArea):
        if communityareas==None: communityareas=[g]
        else: communityareas.append(g)
      if isinstance(g,Municipality):
        if municipalities==None: municipalities=[g]
        else: municipalities.append(g)
  tracts = get_tracts_and_weights(tracts,communityareas,municipalities,wards)
  pops = get_tract_characteristic('pop',tracts.keys())
  vals = get_tract_characteristic(characteristic,tracts.keys())
  norm = sum([pops[i]*tracts[i] for i in pops.keys()])
  return sum([pops[i]*tracts[i]*vals[i] for i in pops.keys()])/norm \
    if norm > 0 else 0

def cache_census_indicators():
  # First, compute the segregation index.
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
    
  # Now do total population.
  for geom_type,geom_str in \
    zip([CensusTract,Municipality,Ward,CommunityArea],\
        ['Census Tract', 'Municipality', 'Ward', 'Community Area']):
    for geom in geom_type.objects.all():
      cv = IndicatorCache(\
        area_type=geom_str, area_id = geom.id,\
        indicator_name = 'pop',\
        indicator_value = get_population(geoms=geom))
      cv.save()

  # Now a bunch of other indicators.
  for indicator in ['median_age', 'pct_18plus', 'pct_65plus', 'pct_whitenh',\
                    'pct_blacknh', 'pct_asiannh', 'pct_hispanic', 'pct_owner_occupied',\
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

def cache_indicators():
  IndicatorCache.objects.all().delete()
  cache_census_indicators()
      

from models import \
  CommunityArea, Ward, CensusTract, Municipality, \
  CensusTractMapping, AreaPlotCache, CensusTractCharacteristics, \
  IndicatorCache
import json
import numpy as np

def iterable(obj):
  '''If it's a scalar, make it a 1-item list. Otherwise do nothing.'''
  try:    iter(obj)
  except: return [obj]
  return obj

def get_tract_characteristic(characteristic, tracts):
  '''Get a value from the characteristics table for a census tract.'''
  retval = {}
  for tract in iterable(tracts):
    tc = CensusTractCharacteristics.objects.get(\
      fips=tract.fips)
    retval[tract] = getattr(tc,characteristic)
    if retval[tract] is None: retval[tract]=0.0
  return retval

def get_tract_from_fips(fips):
  '''Map a fips code to a census tract.'''
  return CensusTract.objects.get(fips__exact=fips)

def get_tracts_and_weights(\
  tracts=None, communityareas=None,\
  municipalities=None, wards=None):
  '''Pull the mapping from census tract to geometry out of the
     CensusTractMapping table. You can pass in any or several
     geometries at once.'''
  retval = {}
  # First deal with any actual census tracts that were passed in.
  if tracts is not None:
    for tract in iterable(tracts):
      retval[tract]=1.0
  # Now step through the other geometries and use the pre-computed
  # mapping to derive the percentage of population of each census tract
  # that should be included for the specified boundaries.
  if communityareas is not None:
    for ca in iterable(communityareas):
      t = ca.censustractmapping_set.all()
      for i in t: 
        thistract = get_tract_from_fips(i.fips)
        # If this tract hasn't already been specified, add it to the output.
        if thistract not in retval.keys(): retval[thistract]=i.communityarea_frac
        # If it has been specified by some other geometry argument, 
        # take the larger of the two fractions. This is a little 
        # sloppy, since it could be a different portion of the community
        # area you've specified already. We should be taking the union.
        # But that's hard, and so far the only use case for this function
        # is for a single geometry type. So this code is dead letter for now anyway.
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
  ''' Get the population of a given geometry. If you want me to try to
      infer the geometry type, use the geoms argument. '''
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
  # Unpack the given geometry(ies) into tracts, and get the multiplicitive
  # factor for which fraction of the tract should be included.
  tracts = get_tracts_and_weights(tracts,communityareas,municipalities,wards)
  # Get the population for each tract.
  pops = get_tract_characteristic('pop',tracts.keys())
  # Population should be an integer.
  return int(sum([pops[i]*tracts[i] for i in pops.keys()]))

def get_pop_weighted_characteristic(characteristic,
  tracts=None, communityareas=None,\
  municipalities=None, wards=None, geoms=None):
  ''' Get some characteristic of a given geometry. If you want me to try to
      infer the geometry type, use the geoms argument. '''
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
  # First get the multiplicitive factor for which fraction of each tract
  # should be included.
  tracts = get_tracts_and_weights(tracts,communityareas,municipalities,wards)
  # Now get the populations...
  pops = get_tract_characteristic('pop',tracts.keys())
  # And the characteristic in question.
  vals = get_tract_characteristic(characteristic,tracts.keys())
  # Here's the normalization factor, which we pre-compute to do a divide-by-zero test.
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
      

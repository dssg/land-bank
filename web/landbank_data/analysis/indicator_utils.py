from models import \
  CommunityArea, Ward, CensusTract, Municipality, \
  CensusTractMapping, AreaPlotCache, CensusTractCharacteristics, \
  IndicatorCache, Foreclosure, Assessor, Transaction
import json
import numpy as np

def indicator_hist(area_type, indicator_name, notzero=True, nbins=10):
  myinds = IndicatorCache.objects.filter(area_type__exact=area_type).\
           filter(indicator_name__exact=indicator_name)
  if notzero:
    myinds = myinds.filter(indicator_value__gt=0)

  retval = [i.indicator_value for i in myinds]
  values, bins = np.histogram(retval,bins=nbins)
  return values, [bins[i]+(bins[i+1]-bins[i])/2.0 for i in range(len(values))]

def percentile(values, thisvalue):
  return int(sum(np.array(values) <= thisvalue)/float(len(values))*100)

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

def get_pop_weighted_characteristic(characteristic,\
  tracts=None, communityareas=None,\
  municipalities=None, wards=None, geoms=None):
  ''' Get some characteristic of a given geometry. If you want me to try to
      infer the geometry type, use the geoms argument. '''
  if geoms is not None:
    tracts, wards, communityareas, municipalities = unpack_geoms(geoms,\
      tracts=tracts, communityareas=communityareas, municipalities=municipalities,\
      wards=wards)
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

def unpack_geoms(geoms,\
  tracts=None, communityareas=None,\
  municipalities=None, wards=None):
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
  return tracts, wards, communityareas, municipalities

def unite_geoms(\
  tracts=None, communityareas=None,\
  municipalities=None, wards=None):
  mygeo=None
  for tract in iterable(tracts):
    if tract is None: continue
    if mygeo is None: mygeo = tract.loc
    mygeo = tract.loc.union(mygeo)
  for communityarea in iterable(communityareas):
    if communityarea is None: continue
    if mygeo is None: mygeo = communityarea.geom
    mygeo = communityarea.geom.union(mygeo)
  for ward in iterable(wards):
    if ward is None: continue
    if mygeo is None: mygeo = ward.geom
    mygeo = ward.geom.union(mygeo)
  for muni in iterable(municipalities):
    if muni is None: continue
    if mygeo is None: mygeo = muni.geom
    mygeo = muni.geom.union(mygeo)
  return mygeo

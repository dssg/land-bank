from models import \
  CommunityArea, Ward, CensusTract, Municipality, \
  CensusTractMapping, AreaPlotCache, CensusTractCharacteristics, \
  IndicatorCache
import json
import numpy as np
import indicators
from indicator_utils import *

def cache_census_indicators():
  indicators.cache_population()
  indicators.cache_segregation()
  indicators.cache_census()

def cache_indicators():
  IndicatorCache.objects.all().delete()
  cache_census_indicators()
      

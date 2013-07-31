import os, csv
from models import CensusTract
from django.contrib.gis.utils import LayerMapping

censustract_mapping = {
  'fips'    : 'GEOID10',
  'loc'      : 'MULTIPOLYGON'
}

censustract_shp = '/mnt/ebs/data/census/tl_2010_17031_tract10/tl_2010_17031_tract10.shp'

def run(verbose = True):
  lm = LayerMapping(CensusTract, censustract_shp, censustract_mapping,\
                    transform=True)
  lm.save(strict=True, verbose=verbose)

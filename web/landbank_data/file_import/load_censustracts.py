import os, csv
from models import CensusTract
from django.contrib.gis.utils import LayerMapping

censustract_mapping = {
  'geoid'    : 'GEOID10',
  'commarea' : 'COMMAREA',
  'loc'      : 'MULTIPOLYGON'
}

censustract_shp = '/mnt/ebs/data/census/censustracts.2010/CensusTractsTIGER2010.shp'

def run(verbose = True):
  lm = LayerMapping(CensusTract, censustract_shp, censustract_mapping,\
                    transform=False)
  lm.save(strict=True, verbose=verbose)

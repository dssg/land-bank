import os, csv
from models import Municipality
from django.contrib.gis.utils import LayerMapping

municipality_mapping = {
  'name'    : 'NAME',
  'geom'    : 'MULTIPOLYGON'
}

municipality_shp = '/mnt/ebs/data/tribapps-gis/shapefiles/census_places/tl_2009_17_place.shp'

def run(verbose = True):
  lm = LayerMapping(Municipality, municipality_shp, municipality_mapping,\
                    transform=True)
  lm.save(strict=True, verbose=verbose)

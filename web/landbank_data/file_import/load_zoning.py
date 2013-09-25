import os, csv
from models import ZoningPolygon
from django.contrib.gis.utils import LayerMapping

zoning_mapping = {
  'zone_class': 'ZONE_CLASS',
  'zone_type' : 'ZONE_TYPE',
  'geom'      : 'MULTIPOLYGON'
}

zoning_shp = '/mnt/ebs/data/zoning/Zoning_nov2012.shp'

def run(verbose = True):
  lm = LayerMapping(ZoningPolygon, zoning_shp, zoning_mapping,\
                    transform=True)
  lm.save(strict=True, verbose=verbose)

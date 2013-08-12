import os, csv
from models import CensusBlock
from django.contrib.gis.utils import LayerMapping

censusblock_mapping = {
  'fips'        : 'GEOID',
  'loc'         : 'MULTIPOLYGON'
}

censusblock_shp = '/mnt/ebs/data/tl_2012_17_tabblock/tl_2012_17_tabblock_cook/tl_2012_17_tabblock.shp'

def run(verbose = True):
  lm = LayerMapping(CensusBlock, censusblock_shp, censusblock_mapping,\
                    transform=True)
  lm.save(strict=True, verbose=verbose)

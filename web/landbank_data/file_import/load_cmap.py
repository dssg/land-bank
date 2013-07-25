import os, csv
from models import CmapPlan
from django.contrib.gis.utils import LayerMapping

cmap_mapping = {
  'name'       : 'LTA_Projec',
  'status'     : 'Status',
  'study_area' : 'StudyArea',
  'short_descr': 'Short_Desc',
  'url'        : 'www',
  'loc'        : 'POLYGON'
}

cmap_shp = '/mnt/ebs/data/cmap/CMAP_LTA_Projects_Cook_07242013.shp'

def run(verbose = True):
  lm = LayerMapping(CmapPlan, cmap_shp, cmap_mapping,\
                    transform=False)
  lm.save(strict=True, verbose=verbose)

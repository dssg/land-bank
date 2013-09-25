#!/usr/bin/env python
import urllib, csv, sys, datetime, cStringIO
from models import BuildingPermit
from django.contrib.gis.geos import Point
from decimal  import Decimal
from pytz import timezone
import os.path, time

chicago_host     = 'data.cityofchicago.org'
permit_view      = 'ydr8-5enu'
permit_file      = '/mnt/ebs/data/permit.csv'

class SocrataClient:
  def __init__(self, hostname, view, outfile):
    self.view       = view
    self.outfile    = outfile
    self.data       = None
    self.header     = None

  def get_data(self):
    urllib.urlretrieve('http://'+chicago_host+'/api/views/'+self.view+\
      '/rows.csv?accessType=DOWNLOAD', self.outfile)
    return self.get_data_from_file()

  def get_data_from_file(self):
    f=open(self.outfile,'r') 
    response_reader = csv.reader(f)
    self.data = []
    self.header = response_reader.next()
    return self.header, response_reader

def run(verbose = True):
  header,data=None,None
  if not os.path.exists(permit_file):
    s = SocrataClient(chicago_host, permit_view, permit_file)
    header,data = s.get_data()
  else:
    s = SocrataClient(chicago_host, permit_view, permit_file)
    header,data = s.get_data_from_file()
  cst = timezone('US/Central')
  skip_lookup = False
  if BuildingPermit.objects.count() == 0:
    skip_lookup = True
  for row in data:
    permit_number    = row[1].strip()
    permit_type      = row[2].strip()
    timestamp        = None if row[3].strip()=='' else \
      cst.localize(datetime.datetime.strptime(row[3], '%m/%d/%Y'))
    try:
      cost           = float(row[4].replace('$','').replace(',',''))
    except:
      cost           = 0.0
    descr            = row[12].strip()[:200]
    pin              = row[13].replace('-','')
    loc              = None if row[-3].strip()=='' else \
      Point((Decimal(row[-2]), Decimal(row[-3])),srid=4326)
    if loc is not None: loc.transform(3435)
    try:
      if skip_lookup:
        raise Exception('no lookup')
      permit  = BuildingPermit.objects.get(\
        permit_number    = permit_number,\
        permit_type      = permit_type,\
        timestamp        = timestamp,\
        cost             = cost,\
        descr            = descr,\
        pin              = pin,\
        loc              = loc)
    except:
      permit  = BuildingPermit(
        permit_number    = permit_number,\
        permit_type      = permit_type,\
        timestamp        = timestamp,\
        cost             = cost,\
        descr            = descr,\
        pin              = pin,\
        loc              = loc)
      permit.save()

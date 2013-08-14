#!/usr/bin/env python
import urllib, csv, sys, datetime, cStringIO
from models import BusinessLicense
from django.contrib.gis.geos import Point
from decimal  import Decimal
from pytz import timezone
import os.path, time


chicago_host     = 'data.cityofchicago.org'
license_view      = 'r5kz-chrr'
license_file      = '/mnt/ebs/data/businesslicense.csv'

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
  if not os.path.exists(license_file):
    s = SocrataClient(chicago_host, license_view, license_file)
    header,data = s.get_data()
  else:
    s = SocrataClient(chicago_host, license_view, license_file)
    header,data = s.get_data_from_file()
  cst = timezone('US/Central')
  skip_lookup = False
  if BusinessLicense.objects.count() == 0:
    skip_lookup = True

  for row in data:
    timestamp         = None if row[19].strip()=='' else \
      cst.localize(datetime.datetime.strptime(row[19], '%m/%d/%Y'))
    if timestamp is None or (timestamp < cst.localize(datetime.datetime.now())): continue
    if row[21] != 'AAI': continue
    license_number    = row[15].strip()
    legal_name        = row[4].strip()[:100]
    dba_name          = row[5].strip()[:100]
    descr             = row[14].strip()[:200]
    code              = row[13].strip()
    loc               = None if row[-3].strip()=='' else \
      Point((Decimal(row[-2]), Decimal(row[-3])),srid=4326)
    if loc is not None: loc.transform(3435)
    try:
      if skip_lookup:
        raise Exception('no lookup')
      license  = BusinessLicense.objects.get(\
        license_number   = license_number,\
        legal_name       = legal_name,\
        dba_name         = dba_name,\
        timestamp        = timestamp,\
        code             = code,\
        descr            = descr,\
        loc              = loc)
    except:
      license  = BusinessLicense(
        license_number   = license_number,\
        legal_name       = legal_name,\
        dba_name         = dba_name,\
        timestamp        = timestamp,\
        code             = code,\
        descr            = descr,\
        loc              = loc)
      license.save()

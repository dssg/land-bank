#!/usr/bin/env python
import urllib, csv, sys, datetime, cStringIO
from models import CrimeIncident
from django.contrib.gis.geos import Point
from decimal  import Decimal
from pytz import timezone
import os.path, time


chicago_host    = 'data.cityofchicago.org'
crime_view      = 'ijzp-q8t2'
crime_file      = '/mnt/ebs/data/crime/crime.csv'

class SocrataClient:
  def __init__(self, hostname, view, outfile):
    self.view       = view
    self.outfile    = outfile
    self.data       = None
    self.header     = None

  def get_data(self):
    urllib.urlretrieve('http://'+chicago_host+'/api/views/'+self.view+\
      '/rows.csv?accessType=DOWNLOAD', self.outfile)
    return get_data_from_file()

  def get_data_from_file(self):
    f=open(self.outfile,'r') 
    response_reader = csv.reader(f)
    self.data = []
    self.header = response_reader.next()
    return self.header, response_reader

def run(verbose = True):
  header,data=None,None
  if not os.path.exists(crime_file):
    s = SocrataClient(chicago_host, crime_view, crime_file)
    header,data = s.get_data()
  else:
    s = SocrataClient(chicago_host, crime_view, crime_file)
    header,data = s.get_data_from_file()
  cst = timezone('US/Central')
  for row in data:
    crimeid   = row[0]
    caseno    = '-' if row[1].strip()=='' else row[1]
    timestamp = cst.localize(datetime.datetime.strptime(row[2], '%m/%d/%Y %I:%M:%S %p'))
    block     = row[3]
    iucr      = row[4]
    ptype     = row[5][:14]
    descr     = row[6][:99]
    locdescr  = row[7][:99]
    arrest    = True if row[8].lower()=='true' else False
    domestic  = True if row[9].lower()=='true' else False
    beat      = int(row[10])
    district  = None if row[11].strip()=='' else int(row[11])
    ward      = None if row[12].strip()=='' else int(row[12])
    commarea  = None if row[13].strip()=='' else int(row[13])
    fbicode   = row[14][:14]
    loc       = None if row[15].strip()=='' else Point((Decimal(row[15]), Decimal(row[16])))
   
    try:
      crime  = CrimeIncident.objects.get(\
        crimeid    = crimeid,\
        caseno     = caseno,\
        timestamp  = timestamp,\
        block      = block,\
        iucr       = iucr,\
        ptype      = ptype,\
        descr      = descr,\
        locdescr   = locdescr,\
        arrest     = arrest,\
        domestic   = domestic,\
        beat       = beat,\
        district   = district,\
        ward       = ward,\
        commarea   = commarea,\
        fbicode    = fbicode,\
        loc        = loc)
    except:
      crime  = CrimeIncident(
        crimeid    = crimeid,\
        caseno     = caseno,\
        timestamp  = timestamp,\
        block      = block,\
        iucr       = iucr,\
        ptype      = ptype,\
        descr      = descr,\
        locdescr   = locdescr,\
        arrest     = arrest,\
        domestic   = domestic,\
        beat       = beat,\
        district   = district,\
        ward       = ward,\
        commarea   = commarea,\
        fbicode    = fbicode,\
        loc        = loc)
      crime.save()

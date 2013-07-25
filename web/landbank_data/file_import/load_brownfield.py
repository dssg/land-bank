#!/usr/bin/env python
import urllib, csv, sys, datetime, cStringIO
from models import Brownfield
from django.contrib.gis.geos import Point
from decimal  import Decimal
from pytz import timezone

brownfield_file = '/mnt/ebs/data/advanced_brownfields_property_list.csv'

def run(verbose = True):
  f = open(brownfield_file,'r')
  csvreader = csv.reader(f)
  cst = timezone('US/Central')
  header = csvreader.next()
  for row in csvreader:
    pins        = '' if row[12] == '' else row[12].replace('-','').replace(';',',')
    recipient   = row[0]
    agreementno = row[2]
    granttype   = row[3]
    fundingtype = row[4]
    acresid     = row[5]
    loc       = None if row[18].strip()=='' else Point((Decimal(row[18]), Decimal(row[17])))
    for pin in [i.strip() for i in pins.split(',')]:
     if len(pin)==10: pin=pin+'0000'
     if len(pin)!=14: 
       print('Found bad PIN: '+pin)
       pin=None
     try:
      brownfield  = Brownfield.objects.get(\
        pin         = pin,\
        recipient   = recipient,\
        agreementno = agreementno,\
        granttype   = granttype,\
        fundingtype = fundingtype,\
        acresid     = acresid,\
        loc         = loc)
     except:
      brownfield  = Brownfield(
        pin         = pin,\
        recipient   = recipient,\
        agreementno = agreementno,\
        granttype   = granttype,\
        fundingtype = fundingtype,\
        acresid     = acresid,\
        loc        = loc)
      brownfield.save()

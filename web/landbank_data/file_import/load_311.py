import os, csv
from models import Vacancy311
from decimal import Decimal
from django.contrib.gis.geos import Point
import datetime

file_311 = '/mnt/ebs/data/311/311_Service_Requests_-_Vacant_and_Abandoned_Buildings_Reported.csv'

def run(verbose = True):
  load_vacancyreport(file_311, verbose = verbose)

def load_vacancyreport(file_311, verbose = False):
  with open(file_311,'r') as f:
    reader = csv.reader(f)
    reader.next()
    for row in reader:
      request_no   = row[1]
      request_date = None
      try:    request_date = datetime.date.strptime(row[2], '%m/%d/%Y')
      except: pass
      bldg_loc     = row[3][0:49]
      hazardous    = row[4][0:49]
      boarded      = row[5][0:49]
      entry_point  = row[6][0:299]
      occupied     = row[7]
      fire         = True if row[8]=='true' else False
      in_use       = True if row[9]=='true' else False
      houseno      = row[10][0:9]
      direction    = row[11]
      street       = row[12]
      suffix       = row[13][0:9]
      zipcode      = None
      try:    zipcode = int(row[14])
      except: pass
      loc          = None if row[15]=='' else Point((Decimal(row[15]), Decimal(row[16])))
      ward         = None
      try:    ward = int(row[17])
      except: pass
      policedistrict=None
      try:    policedistrict = int(row[18])
      except: pass
      ca_num       = None
      try:    ca_num = int(row[19])
      except: pass
      latitude, longitude = None, None
      try:    latitude, longitude = Decimal(row[20]), Decimal(row[21])
      except: pass

      try:
        vacancyreport = Vacancy311.objects.get(\
        request_no    =   request_no   ,\
        request_date  =   request_date ,\
        bldg_loc      =   bldg_loc     ,\
        hazardous     =   hazardous    ,\
        boarded       =   boarded      ,\
        entry_point   =   entry_point  ,\
        occupied      =   occupied     ,\
        fire          =   fire         ,\
        in_use        =   in_use       ,\
        houseno       =   houseno      ,\
        direction     =   direction    ,\
        street        =   street       ,\
        suffix        =   suffix       ,\
        zipcode       =   zipcode      ,\
        loc           =   loc          ,\
        ward          =   ward         ,\
        policedistrict=   policedistrict,\
        ca_num        =   ca_num       ,\
        latitude      =   latitude     ,\
        longitude     =   longitude    \
        )
      except:
        vacancyreport =  Vacancy311(\
        request_no    =   request_no   ,\
        request_date  =   request_date ,\
        bldg_loc      =   bldg_loc     ,\
        hazardous     =   hazardous    ,\
        boarded       =   boarded      ,\
        entry_point   =   entry_point  ,\
        occupied      =   occupied     ,\
        fire          =   fire         ,\
        in_use        =   in_use       ,\
        houseno       =   houseno      ,\
        direction     =   direction    ,\
        street        =   street       ,\
        suffix        =   suffix       ,\
        zipcode       =   zipcode      ,\
        loc           =   loc          ,\
        ward          =   ward         ,\
        policedistrict=   policedistrict,\
        ca_num        =   ca_num       ,\
        latitude      =   latitude     ,\
        longitude     =   longitude    \
        )
      vacancyreport.save()

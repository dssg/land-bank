import os, csv
from load_utils import spss_to_posix
from models import CashFin
from decimal import Decimal
from django.contrib.gis.geos import Point

cashfin_file = '/mnt/ebs/data/repdata_cash_fin_2012_Fellows.tsv' 

def run(verbose = True):
  load_cashfin(cashfin_file, verbose = verbose)

def load_cashfin(cashfin_file, verbose = False):
  with open(cashfin_file,'r') as f:
    reader = csv.reader(f, delimiter="\t")
    reader.next()
    #i = 0;
    skip_lookup = False
    if CashFin.objects.count() == 0:
      skip_lookup = True
    for row in reader:
      #if (i==10):
        #break
      pin = '{:0>14}'.format(int(Decimal(row[1])))
      doc = row[2]
      date_doc = spss_to_posix(row[3])
      date_rec = spss_to_posix(row[4])
      try:	year = int(row[5])
      except:	year = None
      try: 	amount_prime = float(row[6])
      except:   amount_prime = None
      likely_distressed  = True if int(row[7])==1 else False
      likely_cash = True if int(row[8])==1 else False
      buyer = row[9].strip()
      buyer_type = row[10].strip()
      seller = row[11].strip()
      seller_type = row[12].strip()
      apt = row[13].strip()
      direction = row[14].strip()
      houseno = row[15].strip()
      street = row[16].strip()
      suffix = row[17].strip()
      addr_final = row[18].strip()
      city_final = row[19].strip()
      try:	lat_y = float(row[20])
      except:	lat_y = None
      try:	long_x = float(row[21])
      except:	long_x = None
      try:	tract_fix = float(row[22])
      except:	tract_fix = None
      no_tract_info = True if int(row[23])==1 else False
      try:	ca_num = int(row[24])
      except:	ca_num = None
      ca_name = row[25].strip()
      place = row[26].strip()
      gisdate = row[27].strip()
      try: 	ptype_id = int(row[28])
      except:   ptype_id = None
      try:	residential = int(row[29])
      except:	residential = None
      loc       = None if row[20]=='' else Point((Decimal(row[21]), Decimal(row[20])))
      try:
        if skip_lookup:
          raise Exception('no lookup')
        cashfin =  CashFin.objects.get(\
        pin = pin\
        ,doc = doc\
        ,date_doc = date_doc\
	,date_rec = date_rec\
	,year = year\
	,amount_prime = amount_prime\
	,likely_distressed  = likely_distressed\
	,likely_cash = likely_cash\
	,buyer = buyer\
	,buyer_type = buyer_type\
	,seller = seller\
	,seller_type = seller_type\
	,apt = apt\
	,direction = direction\
	,houseno = houseno\
	,street = street\
	,suffix = suffix\
	,addr_final = addr_final\
	,city_final = city_final\
	,lat_y = lat_y\
	,long_x = long_x\
	,tract_fix = tract_fix\
	,no_tract_info = no_tract_info\
	,ca_num = ca_num\
	,ca_name = ca_name\
	,place = place\
	,gisdate = gisdate\
	,ptype_id = ptype_id\
	,residential = residential\
        ,loc = loc\
        )
      except:
        cashfin =  CashFin(\
        pin = pin\
        ,doc = doc\
        ,date_doc = date_doc\
	,date_rec = date_rec\
	,year = year\
	,amount_prime = amount_prime\
	,likely_distressed  = likely_distressed\
	,likely_cash = likely_cash\
	,buyer = buyer\
	,buyer_type = buyer_type\
	,seller = seller\
	,seller_type = seller_type\
	,apt = apt\
	,direction = direction\
	,houseno = houseno\
	,street = street\
	,suffix = suffix\
	,addr_final = addr_final\
	,city_final = city_final\
	,lat_y = lat_y\
	,long_x = long_x\
	,tract_fix = tract_fix\
	,no_tract_info = no_tract_info\
	,ca_num = ca_num\
	,ca_name = ca_name\
	,place = place\
	,gisdate = gisdate\
	,ptype_id = ptype_id\
	,residential = residential\
        ,loc = loc\
        )
      #i += 1
      cashfin.save()

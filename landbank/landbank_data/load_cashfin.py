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
    for row in reader:
      #if (i==10):
        #break
      try:
        cashfin =  CashFin.objects.get(\
        pin     = row[1]\
        ,doc    = row[2]\
        ,date_doc = spss_to_posix(row[3])\
	,date_rec = spss_to_posix(row[4])\
	,year = row[5]\
	,amount_prime = row[6]\
	,likely_distressed  = True if row[7]==1 else False\
	,likely_cash = True if row[8]==1 else False\
	,buyer = row[9].strip()\
	,buyer_type = row[10].strip()\
	,seller = row[11].strip()\
	,seller_type = row[12].strip()\
	,apt = row[13].strip()\
	,direction = row[14].strip()\
	,houseno = row[15].strip()\
	,street = row[16].strip()\
	,suffix = row[17].strip()\
	,addr_final = row[18].strip()\
	,city_final = row[19].strip()\
	,lat_y = row[20]\
	,long_x = row[21]\
	,tract_fix = row[22]\
	,no_tract_info = row[23]\
	,ca_num = row [24]\
	,ca_name = row[25].strip()\
	,place = row[26].strip()\
	,gisdate = row[27].strip()\
	,ptype = row[28]\
	,residential = row[29]\
        ,loc       = None if row[20]=='' else Point((Decimal(row[21]), Decimal(row[20])))\
        )
      except:
        cashfin =  CashFin(\
        pin     = row[1]\
        ,doc    = row[2]\
        ,date_doc = spss_to_posix(row[3])\
	,date_rec = spss_to_posix(row[4])\
	,year = row[5]\
	,amount_prime = row[6]\
	,likely_distressed  = True if row[7]==1 else False\
	,likely_cash = True if row[8]==1 else False\
	,buyer = row[9].strip()\
	,buyer_type = row[10].strip()\
	,seller = row[11].strip()\
	,seller_type = row[12].strip()\
	,apt = row[13].strip()\
	,direction = row[14].strip()\
	,houseno = row[15].strip()\
	,street = row[16].strip()\
	,suffix = row[17].strip()\
	,addr_final = row[18].strip()\
	,city_final = row[19].strip()\
	,lat_y = row[20]\
	,long_x = row[21]\
	,tract_fix = row[22]\
	,no_tract_info = row[23]\
	,ca_num = row [24]\
	,ca_name = row[25].strip()\
	,place = row[26].strip()\
	,gisdate = row[27].strip()\
	,ptype = row[28]\
	,residential = row[29]\
        ,loc       = None if row[20]=='' else Point((Decimal(row[21]), Decimal(row[20])))\
        )
      #i += 1
      cashfin.save()

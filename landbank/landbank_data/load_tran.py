import os, csv
from load_utils import spss_to_posix
from models import Transaction
from decimal import Decimal
from django.contrib.gis.geos import Point

transaction_file = '/mnt/ebs/data/repdata_tran_2012q4_Fellows.tsv'

def run(verbose = True):
  load_transactions(transaction_file, verbose = verbose)

def load_transactions(transaction_file, verbose = False):
  with open(transaction_file,'r') as f:
    reader = csv.reader(f, delimiter="\t")
    reader.next()
    #i = 0;
    for row in reader:
      #if (i==10):
        #break
      try:
        transaction =  Transaction.objects.get(\
        pin     = '{:0>14}'.format(int(Decimal(row[1])))\
	,amount_prime = row[2] if row[2].isdigit() else None\
        ,doc    = row[3]\
        ,date_doc = spss_to_posix(row[4])\
	,date_rec = spss_to_posix(row[5])\
	,buyer = row[6].strip()\
	,buyer_type = row[7].strip()\
	,seller = row[8].strip()\
	,seller_type = row[9].strip()\
	,non_condo = True if row[10] == 1 else False\
	,purchase_less_20k = True if row[11] == 1 else False\
	,business_buyer = True if row[12] == 1 else False\
        ,yq_doc = row[13]\
	,yeard = row[14]\
	,apt = row[15].strip()\
	,direction = row[16].strip()\
	,houseno = row[17].strip()\
	,street = row[18].strip()\
	,suffix = row[19].strip()\
	,addr_final = row[20].strip()\
	,city_final = row[21].strip()\
	,lat_y = row[22]\
	,long_x = row[23]\
	,tract_fix = row[24]\
	,no_tract_info = row[25]\
	,ca_num = row [26]\
	,ca_name = row[27].strip()\
	,place = row[28].strip()\
	,gisdate = row[29].strip()\
	,ptype = row[30]\
	,residential = row[31]\
	,adj_yq = row[32]\
	,adj_yd = row[33]\
        ,loc       = None if row[22]=='' else Point((Decimal(row[23]), Decimal(row[22])))\
        )
      except:
        transaction =  Transaction(\
        pin     = '{:0>14}'.format(int(Decimal(row[1])))\
	,amount_prime = row[2] if row[2].isdigit() else None\
        ,doc    = row[3]\
        ,date_doc = spss_to_posix(row[4])\
	,date_rec = spss_to_posix(row[5])\
	,buyer = row[6].strip()\
	,buyer_type = row[7].strip()\
	,seller = row[8].strip()\
	,seller_type = row[9].strip()\
	,non_condo = True if row[10] == 1 else False\
	,purchase_less_20k = True if row[11] == 1 else False\
	,business_buyer = True if row[12] == 1 else False\
        ,yq_doc = row[13]\
	,yeard = row[14]\
	,apt = row[15].strip()\
	,direction = row[16].strip()\
	,houseno = row[17].strip()\
	,street = row[18].strip()\
	,suffix = row[19].strip()\
	,addr_final = row[20].strip()\
	,city_final = row[21].strip()\
	,lat_y = row[22]\
	,long_x = row[23]\
	,tract_fix = row[24]\
	,no_tract_info = row[25]\
	,ca_num = row [26]\
	,ca_name = row[27].strip()\
	,place = row[28].strip()\
	,gisdate = row[29].strip()\
	,ptype = row[30]\
	,residential = row[31]\
	,adj_yq = row[32]\
	,adj_yd = row[33]\
        ,loc       = None if row[22]=='' else Point((Decimal(row[23]), Decimal(row[22])))\
        )
      #i += 1
      transaction.save()

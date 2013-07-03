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
      pin     = '{:0>14}'.format(int(Decimal(row[1])))
      try:	amount_prime = float(row[2])
      except:	amount_prime = None
      doc    = row[3].strip()
      date_doc = spss_to_posix(row[4])
      date_rec = spss_to_posix(row[5])
      buyer = row[6].strip()
      buyer_type = row[7].strip()
      seller = row[8].strip()
      seller_type = row[9].strip()
      try:	non_condo = int(row[10])
      except:	non_condo = None
      try:	purchase_less_20k = int(row[11])
      except:	purchase_less_20k = None
      try:	business_buyer = int(row[12])
      except:	business_buyer = None
      try:	yq_doc = int(row[13])
      except:   yq_doc = None
      try:	yeard = int(row[14])
      except:   yeard = None
      apt = row[15].strip()
      direction = row[16].strip()
      houseno = row[17].strip()
      street = row[18].strip()
      suffix = row[19].strip()
      addr_final = row[20].strip()
      city_final = row[21].strip()
      try:	lat_y = float(row[22])
      except:	lat_y = None
      try:	long_x = float(row[23])
      except:   long_x = None
      try:	tract_fix = float(row[24])
      except:	tract_fix = None
      no_tract_info = True if int(row[25])==1 else False
      try:	ca_num = int(row[26])
      except:	ca_num = None
      ca_name = row[27].strip()
      place = row[28].strip()
      gisdate = row[29].strip()
      try:	ptype = int(row[30])
      except:   ptype = None
      try: 	residential = int(row[31])
      except:	residential = None
      try:	adj_yq = int(row[32])
      except:   adj_yq = None
      try:	adj_yd = int(row[33])
      except:	adj_yd = None
      loc       = None if row[22]=='' else Point((Decimal(row[23]), Decimal(row[22])))
      try:
        transaction =  Transaction.objects.get(\
        pin = pin\
	,amount_prime = amount_prime\
        ,doc = doc\
        ,date_doc = date_doc\
	,date_rec = date_rec\
	,buyer = buyer\
	,buyer_type = buyer_type\
	,seller = seller\
	,seller_type = seller_type\
	,non_condo = non_condo\
	,purchase_less_20k = purchase_less_20k\
	,business_buyer = business_buyer\
        ,yq_doc = yq_doc\
	,yeard = yeard\
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
	,ptype = ptype\
	,residential = residential\
	,adj_yq = adj_yq\
	,adj_yd = adj_yd\
        ,loc = loc\
        )
      except:
        transaction =  Transaction(\
        pin = pin\
	,amount_prime = amount_prime\
        ,doc = doc\
        ,date_doc = date_doc\
	,date_rec = date_rec\
	,buyer = buyer\
	,buyer_type = buyer_type\
	,seller = seller\
	,seller_type = seller_type\
	,non_condo = non_condo\
	,purchase_less_20k = purchase_less_20k\
	,business_buyer = business_buyer\
        ,yq_doc = yq_doc\
	,yeard = yeard\
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
	,ptype = ptype\
	,residential = residential\
	,adj_yq = adj_yq\
	,adj_yd = adj_yd\
        ,loc = loc\
        )
      #i += 1
      transaction.save()

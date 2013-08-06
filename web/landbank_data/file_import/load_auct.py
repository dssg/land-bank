import os, csv
from load_utils import spss_to_posix
from models import Auction
from decimal import Decimal
from django.contrib.gis.geos import Point

auction_file = '/mnt/ebs/data/repdata_auct_2012q4_Fellows.tsv'

def run(verbose = True):
  load_auctions(auction_file, verbose = verbose)

def load_auctions(auction_file, verbose = False):
  with open(auction_file,'r') as f:
    reader = csv.reader(f, delimiter="\t")
    reader.next()
    skip_lookup = False
    if Auction.objects.count() == 0:
      skip_lookup = True
    #i = 0;
    for row in reader:
      #if (i==10):
        #break
      pin     = '{:0>14}'.format(int(Decimal(row[1])))
      doc    = row[2].strip()
      date_doc = spss_to_posix(row[3])
      date_rec = spss_to_posix(row[4])
      reo = True if int(row[5])==1 else False
      buyer = row[6].strip()
      buyer_type = row[7].strip()
      seller = row[8].strip()
      seller_type = row[9].strip()
      try:	yq_doc = int(row[10])
      except:   yq_doc = None
      try:	yeard = int(row[11])
      except:   yeard = None
      apt = row[12].strip()
      direction = row[13].strip()
      houseno = row[14].strip()
      street = row[15].strip()
      suffix = row[16].strip()
      addr_final = row[17].strip()
      city_final = row[18].strip()
      try:    lat_y        = float(row[19])
      except: lat_y        = None
      try:    long_x       = float(row[20])
      except: long_x       = None
      try:	tract_fix    = float(row[21])
      except: tract_fix    = None
      no_tract_info = True if int(row[22])==1 else False
      try:    ca_num = row[23]
      except: ca_num = None
      ca_name = row[24].strip()
      place = row[25].strip()
      gisdate = row[26].strip()
      try:    ptype_id = int(row[27])
      except: ptype_id = None
      try:    residential = int(row[28])
      except: residential = None
      try:    adj_yq = int(row[29])
      except: adj_yq = None
      try:    adj_yd = int(row[30])
      except: adj_yd = None
      loc       = None if row[19]=='' else Point((Decimal(row[20]), Decimal(row[19])))
      try:
        if skip_lookup:
          raise Exception('no lookup')
        auction = Auction.objects.get(\
        pin = pin\
        ,doc = doc\
        ,date_doc = date_doc\
	,date_rec = date_rec\
	,reo = reo\
	,buyer = buyer\
	,buyer_type = buyer_type\
	,seller = seller\
	,seller_type = seller_type\
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
	,ptype_id = ptype_id\
	,residential = residential\
	,adj_yq = adj_yq\
	,adj_yd = adj_yd\
        ,loc = loc\
        )
      except:
        auction =  Auction(\
        pin = pin\
        ,doc = doc\
        ,date_doc = date_doc\
	,date_rec = date_rec\
	,reo = reo\
	,buyer = buyer\
	,buyer_type = buyer_type\
	,seller = seller\
	,seller_type = seller_type\
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
	,ptype_id = ptype_id\
	,residential = residential\
	,adj_yq = adj_yq\
	,adj_yd = adj_yd\
        ,loc = loc\
        )
      #i += 1
      auction.save()

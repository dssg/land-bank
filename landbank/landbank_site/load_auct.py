import os, csv, datetime, pytz, time
from pytz import timezone
from models import Auction
from decimal import Decimal
from django.contrib.gis.geos import Point

auction_file = '/mnt/ebs/data/repdata_auct_2012q4_Fellows.tsv'

utc = pytz.utc
central_tz = timezone('US/Central')
gregorian_diff = (datetime.datetime(1970, 1, 1) - datetime.datetime(1582, 10, 14)).total_seconds()
year_2100 = time.mktime(datetime.datetime(2100,1,1).timetuple())

def run(verbose = True):
  load_auctions(auction_file, verbose = verbose)

def load_auctions(auction_file, verbose = False):
  with open(auction_file,'r') as f:
    reader = csv.reader(f, delimiter="\t")
    reader.next()
    #i = 0;
    for row in reader:
      #if (i==10):
      #  break
      try:
        auction =  Auction.objects.get(\
        pin     = row[1]\
        ,doc    = row[2]\
        ,date_doc = datetime.datetime.fromtimestamp(Decimal(row[3])-Decimal(gregorian_diff)).replace(tzinfo=utc).astimezone(central_tz) if row[3] > year_2100 else row[3]\
	,date_rec = datetime.datetime.fromtimestamp(Decimal(row[4])-Decimal(gregorian_diff)).replace(tzinfo=utc).astimezone(central_tz) if row[4] > year_2100 else row[4]\
	,reo = True if row[5]==1 else False\
	,buyer = row[6].strip()\
	,buyer_type = row[7].strip()\
	,seller = row[8].strip()\
	,seller_type = row[9].strip()\
        ,yq_doc = row[10]\
	,yeard = row[11]\
	,apt = row[12].strip()\
	,direction = row[13].strip()\
	,houseno = row[14].strip()\
	,street = row[15].strip()\
	,suffix = row[16].strip()\
	,addr_final = row[17].strip()\
	,city_final = row[18].strip()\
	,lat_y = row[19]\
	,long_x = row[20]\
	,tract_fix = row[21]\
	,no_tract_info = row[22]\
	,ca_num = row [23]\
	,ca_name = row[24].strip()\
	,place00 = row[25].strip()\
	,gisdate = row[26].strip()\
	,ptype = row[27]\
	,residential = row[28]\
	,adj_yq = row[29]\
	,adj_yd = row[30]\
        ,loc       = None if row[19]=='' else Point((Decimal(row[20]), Decimal(row[19])))\
        )
      except:
        auction =  Auction(\
        pin     = row[1]\
        ,doc    = row[2]\
        ,date_doc = datetime.datetime.fromtimestamp(Decimal(row[3])-Decimal(gregorian_diff)).replace(tzinfo=utc).astimezone(central_tz) if row[3] > year_2100 else row[3]\
	,date_rec = datetime.datetime.fromtimestamp(Decimal(row[4])-Decimal(gregorian_diff)).replace(tzinfo=utc).astimezone(central_tz) if row[4] > year_2100 else row[4]\
	,reo = True if row[5]==1 else False\
	,buyer = row[6].strip()\
	,buyer_type = row[7].strip()\
	,seller = row[8].strip()\
	,seller_type = row[9].strip()\
        ,yq_doc = row[10]\
	,yeard = row[11]\
	,apt = row[12].strip()\
	,direction = row[13].strip()\
	,houseno = row[14].strip()\
	,street = row[15].strip()\
	,suffix = row[16].strip()\
	,addr_final = row[17].strip()\
	,city_final = row[18].strip()\
	,lat_y = row[19]\
	,long_x = row[20]\
	,tract_fix = row[21]\
	,no_tract_info = row[22]\
	,ca_num = row [23]\
	,ca_name = row[24].strip()\
	,place00 = row[25].strip()\
	,gisdate = row[26].strip()\
	,ptype = row[27]\
	,residential = row[28]\
	,adj_yq = row[29]\
	,adj_yd = row[30]\
        ,loc       = None if row[19]=='' else Point((Decimal(row[20]), Decimal(row[19])))\
        )
        #i += 1
      auction.save()

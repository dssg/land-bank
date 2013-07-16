import os, csv
from load_utils import spss_to_posix
from models import Mortgage
from decimal import Decimal
from django.contrib.gis.geos import Point

mortgage_file = '/mnt/ebs/data/repdata_mort_2012q4_Fellows.tsv'

def run(verbose = True):
  load_mortgages(mortgage_file, verbose = verbose)

def load_mortgages(mortgage_file, verbose = False):
  with open(mortgage_file,'r') as f:
    reader = csv.reader(f, delimiter="\t")
    reader.next()
    #i = 0;
    for row in reader:
      #if (i==10):
        #break
      pin = '{:0>14}'.format(int(Decimal(row[1])))
      doc = row[2].strip()
      try:	mort_amt = float(row[3])
      except:	mort_amt = None
      date_doc = spss_to_posix(row[4])
      date_rec = spss_to_posix(row[5])
      borrower1 = row[6].strip()
      borrower1_type = row[7].strip()
      lender1 = row[8].strip()
      lender1_type = row[9].strip()
      lender2 = row[10].strip()
      lender2_type = row[11].strip()
      try:	yq_doc = int(row[12])
      except:	yq_doc = None
      try:	yeard = int(row[13])
      except:	yeard = None
      apt = row[14].strip()
      direction = row[15].strip()
      houseno = row[16].strip()
      street = row[17].strip()
      suffix = row[18].strip()
      addr_final = row[19].strip()
      city_final = row[20].strip()
      try:	lat_y = float(row[21])
      except:	lat_y = None
      try:	long_x = float(row[22])
      except:	long_x = None
      try:	tract_fix = float(row[23])
      except:	tract_fix = None
      no_tract_info = True if int(row[24])==1 else False
      try:	ca_num = int(row[25])
      except:	ca_num = None
      ca_name = row[26].strip()
      place = row[27].strip()
      gisdate = row[28].strip()
      try: 	ptype_id = int(row[29])
      except:	ptype_id = None
      try:	residential = int(row[30])
      except:	residential = None
      try:	adj_yq = int(row[31])
      except:	adj_yq = None
      try:	adj_yd = int(row[32])
      except:	adj_yd = None
      loc       = None if row[21]=='' else Point((Decimal(row[22]), Decimal(row[21])))
      try:
        mortgage =  Mortgage.objects.get(\
        pin = pin\
        ,doc = doc\
	,mort_amt = mort_amt\
        ,date_doc = date_doc\
	,date_rec = date_rec\
	,borrower1 = borrower1\
	,borrower1_type = borrower1_type\
	,lender1 = lender1\
	,lender1_type = lender1_type\
	,lender2 = lender2\
	,lender2_type = lender2_type\
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
        mortgage =  Mortgage(\
        pin = pin\
        ,doc = doc\
	,mort_amt = mort_amt\
        ,date_doc = date_doc\
	,date_rec = date_rec\
	,borrower1 = borrower1\
	,borrower1_type = borrower1_type\
	,lender1 = lender1\
	,lender1_type = lender1_type\
	,lender2 = lender2\
	,lender2_type = lender2_type\
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
      mortgage.save()

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
      try:
        mortgage =  Mortgage.objects.get(\
        pin     = row[1]\
        ,doc    = row[2]\
	,mort_amt = row[3]\
        ,date_doc = spss_to_posix(row[4])\
	,date_rec = spss_to_posix(row[5])\
	,borrower1 = row[6].strip()\
	,borrower1_type = row[7].strip()\
	,lender1 = row[8].strip()\
	,lender1_type = row[9].strip()\
	,lender2 = row[10].strip()\
	,lender2_type = row[11].strip()\
        ,yq_doc = row[12]\
	,yeard = row[13]\
	,apt = row[14].strip()\
	,direction = row[15].strip()\
	,houseno = row[16].strip()\
	,street = row[17].strip()\
	,suffix = row[18].strip()\
	,addr_final = row[19].strip()\
	,city_final = row[20].strip()\
	,lat_y = row[21]\
	,long_x = row[22]\
	,tract_fix = row[23]\
	,no_tract_info = row[24]\
	,ca_num = row [25]\
	,ca_name = row[26].strip()\
	,place = row[27].strip()\
	,gisdate = row[28].strip()\
	,ptype = row[29]\
	,residential = row[30]\
	,adj_yq = row[31]\
	,adj_yd = row[32]\
        ,loc       = None if row[21]=='' else Point((Decimal(row[22]), Decimal(row[21])))\
        )
      except:
        mortgage =  Mortgage(\
        pin     = row[1]\
        ,doc    = row[2]\
	,mort_amt = row[3]\
        ,date_doc = spss_to_posix(row[4])\
	,date_rec = spss_to_posix(row[5])\
	,borrower1 = row[6].strip()\
	,borrower1_type = row[7].strip()\
	,lender1 = row[8].strip()\
	,lender1_type = row[9].strip()\
	,lender2 = row[10].strip()\
	,lender2_type = row[11].strip()\
        ,yq_doc = row[12]\
	,yeard = row[13]\
	,apt = row[14].strip()\
	,direction = row[15].strip()\
	,houseno = row[16].strip()\
	,street = row[17].strip()\
	,suffix = row[18].strip()\
	,addr_final = row[19].strip()\
	,city_final = row[20].strip()\
	,lat_y = row[21]\
	,long_x = row[22]\
	,tract_fix = row[23]\
	,no_tract_info = row[24]\
	,ca_num = row [25]\
	,ca_name = row[26].strip()\
	,place = row[27].strip()\
	,gisdate = row[28].strip()\
	,ptype = row[29]\
	,residential = row[30]\
	,adj_yq = row[31]\
	,adj_yd = row[32]\
        ,loc       = None if row[21]=='' else Point((Decimal(row[22]), Decimal(row[21])))\
        )
      #i += 1
      mortgage.save()

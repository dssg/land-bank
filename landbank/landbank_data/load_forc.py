import os, csv
from load_utils import spss_to_posix
from models import Foreclosure
from decimal import Decimal
from django.contrib.gis.geos import Point

forc_file = '/mnt/ebs/data/repdata_forc_2012q4_Fellows.tsv'

def run(verbose = True):
  load_foreclosures(forc_file, verbose = verbose)

def load_foreclosures(forc_file, verbose = False):
  with open(forc_file,'r') as f:
    reader = csv.reader(f, delimiter="\t")
    reader.next()
    #i = 0;
    for row in reader:
      #if (i==10):
        #break
      try:
        forc = Foreclosure.objects.get(\
        pin     = '{:0>14}'.format(int(Decimal(row[1])))\
	,filing_date   = spss_to_posix(row[2])\
	,case_num1     = row[3]\
	,case_num2     = row[4].strip()\
	,case_num3     = row[5] if row[5].isdigit() else None\
	,defendant_first_name = row[6].strip()\
	,defendant_last_name = row[7].strip()\
	,plantiff      = row[8].strip()\
	,yq_doc        = row[9]\
	,yeard         = row[10]\
	,apt = row[11].strip()\
	,direction = row[12].strip()\
	,houseno = row[13].strip()\
	,street = row[14].strip()\
	,suffix = row[15].strip()\
	,addr_final = row[16].strip()\
	,city_final = row[17].strip()\
	,lat_y = row[18]\
	,long_x = row[19]\
	,tract_fix = row[20]\
	,no_tract_info = row[21]\
	,ca_num = row [22]\
	,ca_name = row[23].strip()\
	,place = row[24].strip()\
	,gisdate = row[25].strip()\
	,ptype = row[26]\
	,residential = row[27]\
	,adj_yq = row[28]\
	,adj_yd = row[29]\
        ,loc       = None if row[18]=='' else Point((Decimal(row[19]), Decimal(row[18])))\
        )
      except:
        forc =  Foreclosure(\
        pin     = '{:0>14}'.format(int(Decimal(row[1])))\
	,filing_date   = spss_to_posix(row[2])\
	,case_num1     = row[3]\
	,case_num2     = row[4].strip()\
	,case_num3     = row[5] if row[5].isdigit() else None\
	,defendant_first_name = row[6].strip()\
	,defendant_last_name = row[7].strip()\
	,plantiff      = row[8].strip()\
	,yq_doc        = row[9]\
	,yeard         = row[10]\
	,apt = row[11].strip()\
	,direction = row[12].strip()\
	,houseno = row[13].strip()\
	,street = row[14].strip()\
	,suffix = row[15].strip()\
	,addr_final = row[16].strip()\
	,city_final = row[17].strip()\
	,lat_y = row[18]\
	,long_x = row[19]\
	,tract_fix = row[20]\
	,no_tract_info = row[21]\
	,ca_num = row [22]\
	,ca_name = row[23].strip()\
	,place = row[24].strip()\
	,gisdate = row[25].strip()\
	,ptype = row[26]\
	,residential = row[27]\
	,adj_yq = row[28]\
	,adj_yd = row[29]\
        ,loc       = None if row[18]=='' else Point((Decimal(row[19]), Decimal(row[18])))\
        )
      #i += 1
      forc.save()

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
      pin     = '{:0>14}'.format(int(Decimal(row[1])))
      filing_date   = spss_to_posix(row[2])
      try:	case_num1 = int(row[3])
      except:	case_num1 = None
      try: 	case_num2 = row[4].strip()
      except:	case_num2 = None
      try:	case_num3 = float(row[5])
      except:	case_num3 = None
      defendant_first_name = row[6].strip()
      defendant_last_name = row[7].strip()
      plaintiff      = row[8].strip()
      try:	yq_doc = int(row[9])
      except:	yq_doc = None
      try:	yeard = int(row[10])
      except:	yeard = None
      apt = row[11].strip()
      direction = row[12].strip()
      houseno = row[13].strip()
      street = row[14].strip()
      suffix = row[15].strip()
      addr_final = row[16].strip()
      city_final = row[17].strip()
      try:	lat_y = float(row[18])
      except:	lat_y = None
      try:	long_x = float(row[19])
      except:	long_x = None
      try:	tract_fix = float(row[20])
      except: 	tract_fix = None
      no_tract_info = True if int(row[21])==1 else False
      try:	ca_num = int(row[22])
      except:	ca_num = None
      ca_name = row[23].strip()
      place = row[24].strip()
      gisdate = row[25].strip()
      try:	ptype_id = int(row[26])
      except:	ptype_id = None
      try:	residential = int(row[27])
      except:	residential = None
      try:	adj_yq = int(row[28])
      except:	adj_yq = None
      try:	adj_yd = int(row[29])
      except:	adj_yd = None
      loc = None if row[18]=='' else Point((Decimal(row[19]), Decimal(row[18])),srid=4326).transform(3435)
      try:
        forc = Foreclosure.objects.get(\
        pin = pin\
	,filing_date   = filing_date\
	,case_num1     = case_num1\
	,case_num2     = case_num2\
	,case_num3     = case_num3\
	,defendant_first_name = defendant_first_name\
	,defendant_last_name = defendant_last_name\
	,plaintiff      = plaintiff\
	,yq_doc        = yq_doc\
	,yeard         = yeard\
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
        forc =  Foreclosure(\
        pin = pin\
	,filing_date   = filing_date\
	,case_num1     = case_num1\
	,case_num2     = case_num2\
	,case_num3     = case_num3\
	,defendant_first_name = defendant_first_name\
	,defendant_last_name = defendant_last_name\
	,plaintiff      = plaintiff\
	,yq_doc        = yq_doc\
	,yeard         = yeard\
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
      forc.save()

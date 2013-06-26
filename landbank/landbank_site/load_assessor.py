import os, csv
from models import Assessor
from decimal import Decimal
from django.contrib.gis.geos import Point

assessor_file = '/mnt/ebs/data/cook_2011.csv'
base_year = 2011	# Year from which these statistics are based; needed to calculate year built

def run(verbose = True):
  load_assessors(assessor_file, verbose = verbose)

def load_assessors(assessor_file, verbose = False):
  with open(assessor_file,'r') as f:
    reader = csv.reader(f, delimiter=",")
    reader.next()
    #i = 0;
    for row in reader:
      #if (i==10):
        #break
      try:
        assessor = Assessor.objects.get(\
	pin                            = row[1]\
	,houseno                       = row[2].strip()\
	,direction                     = row[3].strip()\
	,street                        = row[4].strip()\
	,year_built                    = base_year - int(row[5].strip()) if row[5].isdigit() else None\
	,attic_desc                    = row[6].strip()[:250] if len(row[6].strip()) > 250 else row[6].strip()\
	,basement_desc                 = row[7].strip()[:250] if len(row[7].strip()) > 250 else row[7].strip()\
	,class_description             = row[8].strip()[:250] if len(row[8].strip()) > 250 else row[8].strip()\
	,current_building_assmt        = row[9] if row[9].isdigit() else None\
	,current_land_assmt            = row[10] if row[10].isdigit() else None\
	,current_total_assmt           = row[11] if row[11].isdigit() else None\
	,ext_desc                      = row[12].strip()\
	,garage_desc                   = row[13].strip()\
	,sqft_bldg                     = row[14] if row[14].isdigit() else None\
	,sqft_land                     = row[15] if row[15].isdigit() else None\
	,ptype                         = row[16].strip()\
	,type_pt_sf                    = True if row[17]==1 else False\
	,type_pt_condo                 = True if row[18]==1 else False\
	,type_pt_2_4                   = True if row[19]==1 else False\
	,type_pt_5                     = True if row[20]==1 else False\
	,type_pt_nonres                = True if row[21]==1 else False\
	,type_pt_unknown               = True if row[22]==1 else False\
	,pt_type1_cat                  = int(row[23])\
	,estim_hunit                   = int(row[24])\
	,lat_y                         = Decimal(row[25]) if row[25].isdigit() else None\
	,long_x                        = Decimal(row[26]) if row[26].isdigit() else None\
	,tract_fix                     = row[27] if row[27].isdigit() else None\
	,no_tract_info                 = row[28] if row[28].isdigit() else None\
	,ca_num                        = row[29] if row[29].isdigit() else None\
	,ca_name                       = row[30].strip()\
	,place                         = row[31].strip()\
	,ward                          = int(Decimal(row[32])) if row[32].isdigit() else None\
	,chicago_flag                  = bool(row[33]) if row[33].isdigit() else None\
	,gisdate                       = row [34].strip()\
        ,loc                           = Point((Decimal(row[26]), Decimal(row[25]))) if (row[25].isdigit() and row[26].isdigit()) else None\
        )
      except:
        assessor = Assessor(\
	pin                            = row[1]\
	,houseno                       = row[2].strip()\
	,direction                     = row[3].strip()\
	,street                        = row[4].strip()\
	,year_built                    = base_year - int(row[5].strip()) if row[5].isdigit() else None\
	,attic_desc                    = row[6].strip()[:250] if len(row[6].strip()) > 250 else row[6].strip()\
	,basement_desc                 = row[7].strip()[:250] if len(row[7].strip()) > 250 else row[7].strip()\
	,class_description             = row[8].strip()[:250] if len(row[8].strip()) > 250 else row[8].strip()\
	,current_building_assmt        = row[9] if row[9].isdigit() else None\
	,current_land_assmt            = row[10] if row[10].isdigit() else None\
	,current_total_assmt           = row[11] if row[11].isdigit() else None\
	,ext_desc                      = row[12].strip()\
	,garage_desc                   = row[13].strip()\
	,sqft_bldg                     = row[14] if row[14].isdigit() else None\
	,sqft_land                     = row[15] if row[15].isdigit() else None\
	,ptype                         = row[16].strip()\
	,type_pt_sf                    = True if row[17]==1 else False\
	,type_pt_condo                 = True if row[18]==1 else False\
	,type_pt_2_4                   = True if row[19]==1 else False\
	,type_pt_5                     = True if row[20]==1 else False\
	,type_pt_nonres                = True if row[21]==1 else False\
	,type_pt_unknown               = True if row[22]==1 else False\
	,pt_type1_cat                  = int(row[23])\
	,estim_hunit                   = int(row[24])\
	,lat_y                         = Decimal(row[25]) if row[25].isdigit() else None\
	,long_x                        = Decimal(row[26]) if row[26].isdigit() else None\
	,tract_fix                     = row[27] if row[27].isdigit() else None\
	,no_tract_info                 = row[28] if row[28].isdigit() else None\
	,ca_num                        = row[29] if row[29].isdigit() else None\
	,ca_name                       = row[30].strip()\
	,place                         = row[31].strip()\
	,ward                          = int(Decimal(row[32])) if row[32].isdigit() else None\
	,chicago_flag                  = bool(row[33]) if row[33].isdigit() else None\
	,gisdate                       = row [34].strip()\
        ,loc                           = Point((Decimal(row[26]), Decimal(row[25]))) if (row[25].isdigit() and row[26].isdigit()) else None\
        )
      #i += 1
      assessor.save()


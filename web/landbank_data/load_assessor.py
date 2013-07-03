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
      pin             = '{:0>14}'.format(int(Decimal(row[1])))
      houseno         = row[2].strip()
      direction       = row[3].strip()
      street          = row[4].strip()
      year_built      = base_year - int(row[5].strip()) if row[5].isdigit() else None
      attic_desc      = row[6].strip()[:250] if len(row[6].strip()) > 250 else row[6].strip()
      basement_desc   = row[7].strip()[:250] if len(row[7].strip()) > 250 else row[7].strip()
      class_desc      = row[8].strip()[:250] if len(row[8].strip()) > 250 else row[8].strip()
      try:    current_building_assmt = float(row[9])
      except: current_building_assmt = None
      try:    current_land_assmt     = float(row[10])
      except: current_land_assmt     = None
      try:    current_total_assmt    = float(row[11])
      except: current_total_assmt    = None
      ext_desc             = row[12].strip()
      garage_desc          = row[13].strip()
      try:    sqft_bldg    = float(row[14])
      except: sqft_bldg    = None
      try:    sqft_land    = float(row[15])
      except: sqft_land    = None
      ptype                = row[16].strip()
      type_pt_sf           = 1 if int(row[17])==1 else 0
      type_pt_condo        = 1 if int(row[18])==1 else 0
      type_pt_2_4          = 1 if int(row[19])==1 else 0
      type_pt_5            = 1 if int(row[20])==1 else 0
      type_pt_nonres       = 1 if int(row[21])==1 else 0
      type_pt_unknown      = 1 if int(row[22])==1 else 0
      try:    pt_type1_cat = int(row[23])
      except: pt_type1_cat = None
      try:    estim_hunit  = int(row[24])
      except: estim_hunit  = None
      try:    lat_y        = float(row[25])
      except: lat_y        = None
      try:    long_x       = float(row[26])
      except: long_x       = None
      try:    tract_fix    = Decimal(row[27]) 
      except: tract_fix    = None
      no_tract_info        = True if int(row[28])==1 else False
      try:    ca_num       = Decimal(row[29]) 
      except: ca_num       = None
      ca_name              = row[30].strip()
      place                = row[31].strip()
      try:    ward         = Decimal(row[32])
      except: ward         = None
      chicago_flag         = True if row[33]==1 else False
      gisdate              = row[34].strip()
      if long_x is not None: loc = Point(long_x, lat_y, srid=4326).transform(3435)

      try:
        assessor = Assessor.objects.get(\
        pin                            = pin,\
	houseno                        = houseno,\
	direction                      = direction,\
	street                         = street,\
	year_built                     = year_built,\
	attic_desc                     = attic_desc,\
	basement_desc                  = basement_desc,\
	class_desc                     = class_desc,\
	current_building_assmt         = current_building_assmt,\
	current_land_assmt             = current_land_assmt,\
	current_total_assmt            = current_total_assmt,\
	ext_desc                       = ext_desc,\
	garage_desc                    = garage_desc,\
	sqft_bldg                      = sqft_bldg,\
	sqft_land                      = sqft_land,\
	ptype                          = ptype,\
	type_pt_sf                     = type_pt_sf,\
	type_pt_condo                  = type_pt_condo,\
	type_pt_2_4                    = type_pt_2_4,\
	type_pt_5                      = type_pt_5,\
	type_pt_nonres                 = type_pt_nonres,\
	type_pt_unknown                = type_pt_unknown,\
	pt_type1_cat                   = pt_type1_cat,\
	estim_hunit                    = estim_hunit,\
	lat_y                          = lat_y,\
	long_x                         = long_x,\
	tract_fix                      = tract_fix,\
	no_tract_info                  = no_tract_info,\
	ca_num                         = ca_num,\
	ca_name                        = ca_name,\
	place                          = place,\
	ward                           = ward,\
	chicago_flag                   = chicago_flag,\
	gisdate                        = gisdate,\
        loc                            = loc\
        )
      except:
        assessor = Assessor(\
        pin                            = pin,\
	houseno                        = houseno,\
	direction                      = direction,\
	street                         = street,\
	year_built                     = year_built,\
	attic_desc                     = attic_desc,\
	basement_desc                  = basement_desc,\
	class_desc                     = class_desc,\
	current_building_assmt         = current_building_assmt,\
	current_land_assmt             = current_land_assmt,\
	current_total_assmt            = current_total_assmt,\
	ext_desc                       = ext_desc,\
	garage_desc                    = garage_desc,\
	sqft_bldg                      = sqft_bldg,\
	sqft_land                      = sqft_land,\
	ptype                          = ptype,\
	type_pt_sf                     = type_pt_sf,\
	type_pt_condo                  = type_pt_condo,\
	type_pt_2_4                    = type_pt_2_4,\
	type_pt_5                      = type_pt_5,\
	type_pt_nonres                 = type_pt_nonres,\
	type_pt_unknown                = type_pt_unknown,\
	pt_type1_cat                   = pt_type1_cat,\
	estim_hunit                    = estim_hunit,\
	lat_y                          = lat_y,\
	long_x                         = long_x,\
	tract_fix                      = tract_fix,\
	no_tract_info                  = no_tract_info,\
	ca_num                         = ca_num,\
	ca_name                        = ca_name,\
	place                          = place,\
	ward                           = ward,\
	chicago_flag                   = chicago_flag,\
	gisdate                        = gisdate,\
        loc                            = loc\
        )
      #i += 1
      assessor.save()


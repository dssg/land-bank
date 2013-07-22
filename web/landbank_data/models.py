from django.contrib.gis.db import models

class LoanApplication(models.Model):
  year              = models.IntegerField('2009, 2010, 2011', null=True)
  respondent_id     = models.CharField('10 character identifier', max_length=10, null=True)
  agency_id         = models.IntegerField('OCC, FRS, FDIC, N/A, NCUA, N/A, HUD, N/A, CFPB', null=True)
  loan_type         = models.IntegerField('Conventional, FHA-insured, VA-guaranteed, FSA/RHS', max_length=12, null=True)
  property_type     = models.IntegerField('1-4 family, Manufactured, multifamily', null=True)
  loan_purpose      = models.IntegerField('Purchase, improvement, refinancing', null=True)
  owner_occ         = models.NullBooleanField('Whether property is owner-occupied, if applicable', null=True)
  loan_amt          = models.IntegerField('Dollar amount of loan', null=True) # in thousands, with leading 0s
  preapproval_req   = models.NullBooleanField('Whether pre-approval was requested, if applicable', null=True)
  action_type       = models.IntegerField('Originated, not accepted, denied, withdrawn, incomplete, purchased, preapproval denied, preapproval not accepted', null=True)
  fips              = models.BigIntegerField('Full 11-digit FIPS census tract code with implied decimal point between 2nd and 3rd last digits', null=True) #tract_id (all in format '####.##')
  applicant_income  = models.IntegerField('Gross annual applicant income', null=True) # in thousands, with leading 0s
  purchaser_type    = models.IntegerField('Fannie, Ginnie, Freddie, Farmer, private, commercial bank, life ins/credit union/mortgage bank/finance co., affiliate inst., other; null implies loan not originated or not sold in this calendar year', null=True)
  denial_reason1    = models.IntegerField('Debt-to-income ratio, employment, credit, collateral, insuff. cash, unverifiable info, incomplete credit application, mort ins denied, other', null=True)
  denial_reason2    = models.IntegerField('Debt-to-income ratio, employment, credit, collateral, insuff. cash, unverifiable info, incomplete credit application, mort ins denied, other', null=True)
  denial_reason3    = models.IntegerField('Debt-to-income ratio, employment, credit, collateral, insuff. cash, unverifiable info, incomplete credit application, mort ins denied, other', null=True)
  rate_spread       = models.FloatField('Percent above APR of mortgage rate', null=True) # has leading 0s
  hoepa_status      = models.NullBooleanField('Whether it\'s a HOEPA loan, only for loans originated or purchased', null=True)   # may have NA values
  lien_status       = models.IntegerField('Secured by 1st lien, secured by subordinate lien, not secured, null implies N/A or loan was purchased', null=True) #
  population        = models.IntegerField('Total population in tract', null=True) # has leading 0s and NAs 
  minority_pop_pct  = models.FloatField('Percentage of minority population to total population for tract', null=True) # has leading 0s and NAs
  med_fam_inc       = models.IntegerField('HUD median family income in dollars for the MSA/MD in which the tract is located, adjusted annually by HUD', null=True)
  tract_msa_md_inc  = models.FloatField('Percent of tract median family income compared to MSA/MD median family income', null=True) # has NAs
  num_owner_occ     = models.IntegerField('Number of dwellings, including individual condos, that are lived in by the owner', null=True) # has leading 0s and NAs
  num_1_4           = models.IntegerField('Dwellings that are built to house fewer than 5 families', null=True)  # has leading 0s and NAs
  def __unicode__(self):
    return unicode(self.fips) + u' ' + unicode(self.loan_amt)
  class Meta:
    app_label = 'landbank_data'

class Vacancy311(models.Model):
  request_no     = models.CharField('Request number', max_length=25)
  request_date   = models.DateTimeField('Request date')
  bldg_loc       = models.CharField('Building location', max_length=50)
  hazardous      = models.CharField('Hazardous condition?', max_length=50)
  boarded        = models.CharField('Boarded up?', max_length=50)
  entry_point    = models.CharField('Entry point', max_length=300)
  occupied       = models.CharField('Occupied?', max_length=300)
  fire           = models.NullBooleanField('Vacant due to fire')
  in_use         = models.NullBooleanField('In use?')
  houseno        = models.CharField('House number', max_length=10)
  direction      = models.CharField('Street direction', max_length=2)
  street         = models.CharField('Street name', max_length=100)
  suffix         = models.CharField('Street suffix', max_length=10)
  zipcode        = models.IntegerField('ZIP code')
  loc            = models.PointField(null=True,srid=3435)
  ward           = models.IntegerField('Ward')
  policedistrict = models.IntegerField('Police district')
  ca_num         = models.IntegerField('Community area number')
  latitude       = models.FloatField('Latitude')
  longitude      = models.FloatField('Longitude')
  objects        = models.GeoManager()
  def __unicode__(self):
    return unicode(self.request_no)
  class Meta:
    app_label = 'landbank_data'


class VacancyUSPS(models.Model):
  year          = models.IntegerField('Year')
  quarter       = models.IntegerField('Quarter')
  fips          = models.BigIntegerField('Census tract identifying FIPS number')
  naddr_res     = models.IntegerField('Total number of residential addresses')
  naddr_bus     = models.IntegerField('Total number of business addresses')
  naddr_oth     = models.IntegerField('Total number of other addresses')
  res_vacant    = models.IntegerField('Vacant residential addresses')
  bus_vacant    = models.IntegerField('Vacant business addresses')
  oth_vacant    = models.IntegerField('Vacant other addresses')
  res_vac_avg   = models.IntegerField('Average days residential address have been vacant')
  bus_vac_avg   = models.IntegerField('Average days business address have been vacant')
  res_vac_3     = models.IntegerField('Residential vacant 3 months or less')
  bus_vac_3     = models.IntegerField('Business vacant 3 months or less')
  oth_vac_3     = models.IntegerField('Other vacant 3 months or less')
  res_vac_3_6   = models.IntegerField('Residential vacant 3-6 months')
  bus_vac_3_6   = models.IntegerField('Business vacant 3-6 months')
  oth_vac_3_6   = models.IntegerField('Other vacant 3-6 months')
  res_vac_6_12  = models.IntegerField('Residential vacant 6-12 months')
  bus_vac_6_12  = models.IntegerField('Business vacant 6-12 months')
  oth_vac_6_12  = models.IntegerField('Other vacant 6-12 months')
  res_vac_12_24 = models.IntegerField('Residential vacant 12-24 months')
  bus_vac_12_24 = models.IntegerField('Business vacant 12-24 months')
  oth_vac_12_24 = models.IntegerField('Other vacant 12-24 months')
  res_vac_24_36 = models.IntegerField('Residential vacant 24-36 months')
  bus_vac_24_36 = models.IntegerField('Business vacant 24-36 months')
  oth_vac_24_36 = models.IntegerField('Other vacant 24-36 months')
  res_vac_36    = models.IntegerField('Residential vacant 36+ months')
  bus_vac_36    = models.IntegerField('Business vacant 36+ months')
  oth_vac_36    = models.IntegerField('Other vacant 36+ months')
  pqv_is_res    = models.IntegerField('Residential vacant previous quarter, now in use')
  pqv_is_bus    = models.IntegerField('Business vacant previous quarter, now in use')
  pqv_is_oth    = models.IntegerField('Other vacant previous quarter, now in use')
  pqv_ns_res    = models.IntegerField('Residential vacant previous quarter, now no-stat')
  pqv_ns_bus    = models.IntegerField('Business vacant previous quarter, now no-stat')
  pqv_ns_oth    = models.IntegerField('Other vacant previous quarter, now no-stat')
  res_nostat    = models.IntegerField('No-stat residential addresses')
  bus_nostat    = models.IntegerField('No-stat business addresses')
  oth_nostat    = models.IntegerField('No-stat other addresses')
  res_ns_3      = models.IntegerField('Residential no-stat 3 months or less')
  bus_ns_3      = models.IntegerField('Business no-stat 3 months or less')
  oth_ns_3      = models.IntegerField('Other no-stat 3 months or less')
  res_ns_3_6    = models.IntegerField('Residential no-stat 3-6 months')
  bus_ns_3_6    = models.IntegerField('Business no-stat 3-6 months')
  oth_ns_3_6    = models.IntegerField('Other no-stat 3-6 months')
  res_ns_6_12   = models.IntegerField('Residential no-stat 6-12 months')
  bus_ns_6_12   = models.IntegerField('Business no-stat 6-12 months')
  oth_ns_6_12   = models.IntegerField('Other no-stat 6-12 months')
  res_ns_12_24  = models.IntegerField('Residential no-stat 12-24 months')
  bus_ns_12_24  = models.IntegerField('Business no-stat 12-24 months')
  oth_ns_12_24  = models.IntegerField('Other no-stat 12-24 months')
  res_ns_24_36  = models.IntegerField('Residential no-stat 24-36 months')
  bus_ns_24_36  = models.IntegerField('Business no-stat 24-36 months')
  oth_ns_24_36  = models.IntegerField('Other no-stat 24-36 months')
  res_ns_36     = models.IntegerField('Residential no-stat 36+ months')
  bus_ns_36     = models.IntegerField('Business no-stat 36+ months')
  oth_ns_36     = models.IntegerField('Other no-stat 36+ months')
  pqns_is_res   = models.IntegerField('Residential no-stat previous quarter, now in use')
  pqns_is_bus   = models.IntegerField('Business no-stat previous quarter, now in use')
  pqns_is_oth   = models.IntegerField('Other no-stat previous quarter, now in use')
  def __unicode__(self):
    return unicode(self.fips)
  class Meta:
    app_label = 'landbank_data'


class Auction(models.Model):
  pin           = models.CharField('Property ID number', max_length=14, db_index=True)
  doc           = models.CharField('Recorder of Deeds document number', null=True, max_length=16)
  date_doc      = models.DateTimeField('Date documented', null=True)
  date_rec      = models.DateTimeField('Date recorded', null=True)
  reo           = models.NullBooleanField('Entering REO', null=True)
  buyer         = models.CharField('Buyer name', max_length=100, null=True)
  buyer_type    = models.CharField('Buyer type', max_length=100, null=True)
  seller        = models.CharField('Seller name', max_length=100, null=True)
  seller_type   = models.CharField('Seller type', max_length=100, null=True)
  yq_doc        = models.IntegerField('Year and quarter of RoD document filing', null=True)
  yeard         = models.IntegerField('???', null=True)
  apt           = models.CharField('Apartment numer', max_length=10, null=True)
  direction     = models.CharField('Street direction', max_length=2, null=True)
  houseno       = models.CharField('House number', max_length=10, null=True)
  street        = models.CharField('Street name', max_length=50, null=True)
  suffix        = models.CharField('Street suffix', max_length=10, null=True)
  addr_final    = models.CharField('First line of address', max_length=100, null=True)
  city_final    = models.CharField('City name', max_length=100, null=True)
  lat_y         = models.FloatField('Latitude', null=True)
  long_x        = models.FloatField('Longitude', null=True)
  tract_fix     = models.FloatField('2000 census tract', null=True)
  no_tract_info = models.NullBooleanField('No geography information', null=True)
  ca_num        = models.IntegerField('Community area number', null=True)
  ca_name       = models.CharField('Community area', max_length=100, null=True)
  place         = models.CharField('Cook County subdivision', max_length=100, null=True)
  gisdate       = models.CharField('GIS file reference date', max_length=100, null=True)
  ptype		= models.ForeignKey('PropertyTypes')
  residential   = models.IntegerField('Residential?', null=True)
  adj_yq        = models.IntegerField('Adjusted quarter?', null=True)
  adj_yd        = models.IntegerField('Adjusted day?', null=True)
  loc           = models.PointField(null=True,srid=3435)
  objects       = models.GeoManager()
  def __unicode__(self):
    return unicode(self.pin)
  class Meta:
    app_label = 'landbank_data'


class CashFin(models.Model):
  pin                = models.CharField('Property ID number', max_length=14, db_index=True)
  doc                = models.CharField('Recorder of Deeds document number', null=True, max_length=16)
  date_doc           = models.DateTimeField('Date documented', null=True)
  date_rec           = models.DateTimeField('Date recorded', null=True)
  year               = models.IntegerField('Year of transaction', null=True)
  amount_prime       = models.FloatField('Transaction amount', null=True)
  likely_distressed  = models.NullBooleanField('Property distressed?', null=True)
  likely_cash        = models.NullBooleanField('Transaction cash-only?', null=True)
  buyer              = models.CharField('Buyer name', null=True, max_length=100)
  buyer_type         = models.CharField('Individual or business buyer?', null=True, max_length=100)
  seller             = models.CharField('Seller name', null=True, max_length=100)
  seller_type        = models.CharField('Individual or business seller?', null=True, max_length=100)
  apt                = models.CharField('Apartment number', null=True, max_length=100)
  direction          = models.CharField('Street direction', null=True, max_length=100)
  houseno            = models.CharField('House number', null=True, max_length=100)
  street             = models.CharField('Street name', null=True, max_length=100)
  suffix             = models.CharField('Street suffix', null=True, max_length=100)
  addr_final         = models.CharField('First line of address', null=True, max_length=100)
  city_final         = models.CharField('City name', null=True, max_length=100)
  lat_y              = models.FloatField('Latitude', null=True)
  long_x             = models.FloatField('Longitude', null=True)
  tract_fix          = models.FloatField('2000 census tract', null=True)
  no_tract_info      = models.NullBooleanField('No geography information', null=True)
  ca_num             = models.IntegerField('Community area number', null=True)
  ca_name            = models.CharField('Community area', null=True, max_length=100)
  place              = models.CharField('Cook County subdivision', null=True, max_length=100)
  gisdate            = models.CharField('GIS file reference date', null=True, max_length=100)
  ptype		     = models.ForeignKey('PropertyTypes')
  residential        = models.IntegerField('Residential?', null=True)
  loc           = models.PointField(null=True,srid=3435)
  objects       = models.GeoManager()
  def __unicode__(self):
    return unicode(self.pin)
  class Meta:
    app_label = 'landbank_data'


class Foreclosure(models.Model):
  pin           = models.CharField('Property ID number', max_length=14, db_index=True)
  filing_date   = models.DateTimeField('Date filed', null=True)
  case_num1     = models.IntegerField('Case number', null=True)
  case_num2     = models.CharField('Case number (2)', null=True, max_length=100)
  case_num3     = models.FloatField('Case number (3)', null=True)
  defendant_first_name = models.CharField('First name of defendant', null=True, max_length=100)
  defendant_last_name = models.CharField('Last name of defendant', null=True, max_length=100)
  plaintiff      = models.CharField('Plaintiff name', null=True, max_length=100)
  date_doc      = models.DateTimeField('Date documented', null=True)
  date_rec      = models.DateTimeField('Date recorded', null=True)
  yq_doc        = models.IntegerField('Year and quarter recorded', null=True)
  yeard         = models.IntegerField('Year recorded', null=True)
  apt           = models.CharField('Apartment numer', max_length=10, null=True)
  direction     = models.CharField('Street direction', max_length=2, null=True)
  houseno       = models.CharField('House number', max_length=10, null=True)
  street        = models.CharField('Street name', max_length=50, null=True)
  suffix        = models.CharField('Street suffix', max_length=10, null=True)
  addr_final    = models.CharField('First line of address', max_length=100, null=True)
  city_final    = models.CharField('City name', max_length=100, null=True)
  lat_y         = models.FloatField('Latitude', null=True)
  long_x        = models.FloatField('Longitude', null=True)
  tract_fix     = models.FloatField('2000 census tract', null=True)
  no_tract_info = models.NullBooleanField('No geography information', null=True)
  ca_num        = models.IntegerField('Community area number', null=True)
  ca_name       = models.CharField('Community area', max_length=100, null=True)
  place         = models.CharField('Cook County subdivision', max_length=100, null=True)
  gisdate       = models.CharField('GIS file reference date', max_length=100, null=True)
  ptype	        = models.ForeignKey('PropertyTypes')
  residential   = models.IntegerField('Residential?', null=True)
  adj_yq        = models.IntegerField('Adjusted quarter?', null=True)
  adj_yd        = models.IntegerField('Adjusted day?', null=True)
  loc           = models.PointField(null=True,srid=3435)
  objects       = models.GeoManager()
  def __unicode__(self):
    return unicode(self.pin)
  class Meta:
    app_label = 'landbank_data'


class Mortgage(models.Model):
  pin           = models.CharField('Property ID number', max_length=14, db_index=True)
  doc           = models.CharField('Document ID', null=True, max_length=100)
  mort_amt      = models.FloatField('Mortgage dollar amount', null=True)
  date_doc      = models.DateTimeField('Date documented', null=True)
  date_rec      = models.DateTimeField('Date recorded', null=True)
  borrower1     = models.CharField('Borrower', max_length=100, null=True)
  borrower1_type = models.CharField('Borrower type', max_length=10, null=True) 
  lender1       = models.CharField('Lender', max_length=100, null=True)
  lender1_type  = models.CharField('Type of lender', max_length=10, null=True)
  lender2       = models.CharField('Lender', max_length=100, null=True)
  lender2_type  = models.CharField('Type of lender', max_length=10, null=True)
  yq_doc        = models.IntegerField('Year and quarter recorded', null=True)
  yeard         = models.IntegerField('Year recorded', null=True)
  apt           = models.CharField('Apartment numer', max_length=10, null=True)
  direction     = models.CharField('Street direction', max_length=2, null=True)
  houseno       = models.CharField('House number', max_length=10, null=True)
  street        = models.CharField('Street name', max_length=50, null=True)
  suffix        = models.CharField('Street suffix', max_length=10, null=True)
  addr_final    = models.CharField('First line of address', max_length=100, null=True)
  city_final    = models.CharField('City name', max_length=100, null=True)
  lat_y         = models.FloatField('Latitude', null=True)
  long_x        = models.FloatField('Longitude', null=True)
  tract_fix     = models.FloatField('2000 census tract', null=True)
  no_tract_info = models.NullBooleanField('No geography information', null=True)
  ca_num        = models.IntegerField('Community area number', null=True)
  ca_name       = models.CharField('Community area', max_length=100, null=True)
  place         = models.CharField('Cook County subdivision', max_length=100, null=True)
  gisdate       = models.CharField('GIS file reference date', max_length=100, null=True)
  ptype	        = models.ForeignKey('PropertyTypes')
  residential   = models.IntegerField('Residential?', null=True)
  adj_yq        = models.IntegerField('Adjusted quarter', null=True)
  adj_yd        = models.IntegerField('Adjusted day', null=True)
  loc           = models.PointField(null=True,srid=3435)
  objects       = models.GeoManager()
  def __unicode__(self):
    return unicode(self.pin)
  class Meta:
    app_label = 'landbank_data'


class Transaction(models.Model):
  pin           = models.CharField('Property ID number', max_length=14, db_index=True)
  amount_prime  = models.FloatField('Mortgage amount', null=True) 
  doc		= models.CharField('Document ID', null=True, max_length=100)
  date_doc      = models.DateTimeField('Date documented', null=True)
  date_rec      = models.DateTimeField('Date recorded', null=True)
  buyer		= models.CharField('Buyer', max_length=100, null=True)
  buyer_type	= models.CharField('Buyer type', max_length=10, null=True)
  seller	= models.CharField('Seller', max_length=100, null=True)
  seller_type	= models.CharField('Seller type', max_length=10, null=True)
  non_condo	= models.IntegerField('Not a condo?', null=True) 
  purchase_less_20k = models.IntegerField('Low-value transaction?', null=True) 
  business_buyer = models.IntegerField('Buyer is a business?', null=True) 
  yq_doc        = models.IntegerField('Year and quarter recorded', null=True)
  yeard         = models.IntegerField('Year recorded', null=True)
  apt           = models.CharField('Apartment numer', max_length=10, null=True)
  direction     = models.CharField('Street direction', max_length=2, null=True)
  houseno       = models.CharField('House number', max_length=10, null=True)
  street        = models.CharField('Street name', max_length=50, null=True)
  suffix        = models.CharField('Street suffix', max_length=10, null=True)
  addr_final    = models.CharField('First line of address', max_length=100, null=True)
  city_final    = models.CharField('City name', max_length=100, null=True)
  lat_y         = models.FloatField('Latitude', null=True)
  long_x        = models.FloatField('Longitude', null=True)
  tract_fix     = models.FloatField('2000 census tract', null=True)
  no_tract_info = models.NullBooleanField('No geography information', null=True)
  ca_num        = models.IntegerField('Community area number', null=True)
  ca_name       = models.CharField('Community area', max_length=100, null=True)
  place         = models.CharField('Cook County subdivison', max_length=100, null=True)
  gisdate       = models.CharField('GIS file reference date', max_length=100, null=True)
  ptype	        = models.ForeignKey('PropertyTypes')
  residential   = models.IntegerField('Residential?', null=True)
  adj_yq        = models.IntegerField('Adjusted quarter', null=True)
  adj_yd        = models.IntegerField('Adjusted day', null=True)
  loc           = models.PointField(null=True,srid=3435)
  objects       = models.GeoManager()
  def __unicode__(self):
    return unicode(self.pin)
  class Meta:
    app_label = 'landbank_data'


class Assessor(models.Model):                                         
  pin                           = models.CharField('Property ID number', max_length=14, db_index=True)
  houseno                       = models.CharField('Address number', max_length=100, null=True)
  direction                     = models.CharField('Street direction', max_length=2, null=True)
  street                        = models.CharField('Street name', max_length=100, null=True)
  year_built                    = models.IntegerField('Year the property was built', null=True)
  attic_desc                    = models.CharField('Attic description', max_length=250, null=True)
  basement_desc                 = models.CharField('Basement description', max_length=250, null=True)
  class_desc                    = models.CharField('Building class description', max_length=250, null=True)
  current_building_assmt        = models.FloatField('Current assessment of building', null=True)
  current_land_assmt            = models.FloatField('Current assessment of land', null=True)
  current_total_assmt           = models.FloatField('Current total assessment', null=True)
  ext_desc                      = models.CharField('Extended description', max_length=100, null=True)
  garage_desc                   = models.CharField('Garage description', max_length=100, null=True)
  sqft_bldg                     = models.FloatField('Building square footage', null=True)
  sqft_land                     = models.FloatField('Land square footage', null=True)
  ptype_desc                    = models.CharField('Property type', max_length=100, null=True)
  type_pt_sf                    = models.IntegerField('Single-family', null=True)
  type_pt_condo                 = models.IntegerField('Condo', null=True)
  type_pt_2_4                   = models.IntegerField('2-4 unit building', null=True)
  type_pt_5                     = models.IntegerField('5+ unit building', null=True)
  type_pt_nonres                = models.IntegerField('Non-residental building', null=True)
  type_pt_unknown               = models.IntegerField('Building of unknown type', null=True)
  ptype                         = models.ForeignKey('PropertyTypes')
  estim_hunit                   = models.IntegerField('Estimated number of housing units based on sqft', null=True)
  lat_y                         = models.FloatField('Latitude', null=True)
  long_x                        = models.FloatField('Longitude', null=True)
  tract_fix                     = models.FloatField('2000 census tract', null=True)
  no_tract_info                 = models.NullBooleanField('No geography information', null=True)
  ca_num                        = models.IntegerField('Community area number', null=True)
  ca_name                       = models.CharField('Community area', max_length=100, null=True)
  place                         = models.CharField('Cook County subdivision', max_length=100, null=True)
  ward                          = models.IntegerField('Ward number, if available', null=True)
  chicago_flag                  = models.IntegerField('Within city limits?', null=True)
  gisdate                       = models.CharField('GIS file reference date', max_length=100, null=True)
  loc                           = models.PointField(null=True,srid=3435)
  objects                       = models.GeoManager()
  def __unicode__(self):
    return unicode(self.pin)
  class Meta:
    app_label = 'landbank_data'


class Scavenger(models.Model):
  pin                           = models.CharField('Property ID number', max_length=14, db_index=True)
  township			= models.IntegerField('Township (community area?) ID number', null=True)
  volume			= models.CharField('???', max_length=3, null=True)
  tax_year			= models.IntegerField('Year of tax balance', null=True)
  tax_type			= models.CharField('???', max_length=2, null=True)
  tax_amount			= models.FloatField('???', null=True)
  total_amount			= models.FloatField('???', null=True)
  def __unicode__(self):
    return unicode(self.pin)
  class Meta:
    app_label = 'landbank_data'

class CensusTract(models.Model):
  fips 				= models.BigIntegerField('Census tract identifying FIPS number', null=True)
  commarea                      = models.IntegerField('Community area', null=False)
  loc                           = models.MultiPolygonField(null=False, srid=3435)
  objects                       = models.GeoManager()
  def __unicode__(self):
    return unicode(self.fips)
  class Meta:
    app_label = 'landbank_data'

class SummaryStats(models.Model):
  # identifying characteristics of geographic area and property type segment
  area_number			= models.BigIntegerField('Number, if applicable, of the political area; wards 1-50, areas 1-77, census tract FIPS codes, etc. NOT a foreign key', db_index=True, null=True)
  area_type                     = models.CharField('Descriptor of land area subdivision like ward, census tract, etc.', max_length=30, null=True)
  area_name                     = models.CharField('Name of area subdivision if applicable like Near North Side, Lakeview, etc.', max_length = 50, null=True)
  ptype				= models.ForeignKey('PropertyTypes')

  # summary statistics of properties 
  count				= models.IntegerField('Number of properties in the given geographical and property type segment', null=True)
  bldg_assmt_avg                = models.FloatField('Average building assessed value', null=True)
  land_assmt_avg                = models.FloatField('Average land assessed value', null=True)
  total_assmt_avg               = models.FloatField('Average total assessed value', null=True)
  bldg_sqft_avg			= models.FloatField('Average building square footage', null=True)
  land_sqft_avg			= models.FloatField('Average land plot square footage', null=True)
  ppsf_avg			= models.FloatField('Average price per square foot-single family homes only', null=True)

  objects                       = models.GeoManager()
  def __unicode__(self):
    return unicode(self.area_type) + u' ' + unicode(self.area_id) + u' ptype:' + unicode(self.ptype)
  class Meta:
    app_label = 'landbank_data'

class PropertyTypes(models.Model):
  type_desc			= models.CharField('Description of property type', max_length=30, null=True)

  def __unicode__(self):
    return unicode(self.type_desc)
  class Meta:
    app_label = 'landbank_data'

class Wards(models.Model):
  data_admin			= models.FloatField('???', null=True)
  perimeter			= models.FloatField('???', null=True)
  ward				= models.IntegerField('Ward number, does not match primary key', null=True)
  alderman			= models.CharField('Alderman name', max_length=60, null=True)
  ward_class			= models.IntegerField('???', null=True)
  ward_phone 			= models.CharField('Ward phone number', max_length=12, null=True)
  hall_phone			= models.CharField('???? phone number', max_length=12, null=True)
  hall_office			= models.CharField('???', max_length=45, null=True)
  address			= models.CharField('??? address', max_length=39, null=True)
  edit_date			= models.CharField('Unformatted date of last edit?', max_length=10, null=True)
  shape_area			= models.FloatField('???', null=True)
  shape_len			= models.FloatField('???', null=True)
  geom				= models.MultiPolygonField(null=False, srid=3435)
  objects			= models.GeoManager()
  def __unicode__(self):
    return unicode(self.ward)
  class Meta:
    app_label = 'landbank_data'

class CommunityAreas(models.Model):
  area_number			= models.IntegerField('Community area number', null=True)
  area_name			= models.CharField('Community area name', max_length=80, null=True)
  shape_area			= models.FloatField('???', null=True)
  shape_len			= models.FloatField('???', null=True)
  geom				= models.MultiPolygonField(null=False, srid=3435)
  objects			= models.GeoManager()
  def __unicode__(self):
    return unicode(self.area_number) + u'_' + unicode(self.area_name)
  class Meta:
    app_label = 'landbank_data'

class PinAreaLookup(models.Model):
  pin				= models.CharField('Property ID number', max_length=15, null=False, db_index=True)
  ward_id			= models.IntegerField('Foreign key to landbank_data_wards', null=True, db_index=True)
  community_area_id		= models.IntegerField('Foreign key to landbank_data_communityareas', null=True, db_index=True)
  census_tract_id		= models.IntegerField('Foreign key to landbank_data_censustracts', null=True, db_index=True)
  def __unicode__(self):
    return unicode(self.pin)
  class Meta:
    app_label = 'landbank_data'


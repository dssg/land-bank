from django.contrib.gis.db import models

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
  ptype                         = models.CharField('Property type', max_length=100, null=True)
  type_pt_sf                    = models.IntegerField('Single-family', null=True)
  type_pt_condo                 = models.IntegerField('Condo', null=True)
  type_pt_2_4                   = models.IntegerField('2-4 unit building', null=True)
  type_pt_5                     = models.IntegerField('5+ unit building', null=True)
  type_pt_nonres                = models.IntegerField('Non-residental building', null=True)
  type_pt_unknown               = models.IntegerField('Building of unknown type', null=True)
  pt_type1_cat                  = models.IntegerField('Property type code', null=True)
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


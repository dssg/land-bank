from django.contrib.gis.db import models

class Auction(models.Model):                                         # results of 'dtype' from pandas
  pin           = models.FloatField('Property ID number', db_index=True)            # pin1                    float64
  doc           = models.CharField('???', null=True, max_length=16)                           # doc_num_t1              float64
  date_doc      = models.DateTimeField('Date documented', null=True)            # date_doc_t1             float64
  date_rec      = models.DateTimeField('Date recorded', null=True)              # date_rec_t1             float64
  reo           = models.NullBooleanField('Entering REO', null=True)                # Entering_REO              int64
  buyer         = models.CharField('Buyer name', max_length=100, null=True)     # Buyer1                   object
  buyer_type    = models.CharField('Buyer type', max_length=100, null=True)     # Buyer1_Type              object
  seller        = models.CharField('Seller name', max_length=100, null=True)    # Seller1                  object
  seller_type   = models.CharField('Seller type', max_length=100, null=True)    # Seller1_Type             object
  yq_doc        = models.IntegerField('???', null=True)                         # YYYYQ_DOC                 int64
  yeard         = models.IntegerField('???', null=True)                         # YEARD                     int64
  apt           = models.CharField('Apartment numer', max_length=10, null=True) # APT                      object
  direction           = models.CharField('Street direction', max_length=2, null=True) # DIR                      object
  houseno       = models.CharField('House number', max_length=10, null=True)    # HOUSENO                  object
  street        = models.CharField('Street name', max_length=50, null=True)    # STREET                   object
  suffix        = models.CharField('Street suffix', max_length=10, null=True)   # SUFFIX                   object
  addr_final    = models.CharField('???', max_length=100, null=True)            # ADDR_FINAL               object
  city_final    = models.CharField('???', max_length=100, null=True)            # CITY_FINAL               object
  lat_y         = models.FloatField('Latitude', null=True)                      # LAT_Y                   float64
  long_x        = models.FloatField('Longitude', null=True)                     # LNG_X                   float64
  tract_fix     = models.FloatField('???', null=True)                           # Tract_Fix               float64
  no_tract_info = models.IntegerField('???', null=True)                         # No_Tract_Info             int64
  ca_num        = models.IntegerField('???', null=True)                         # CA_num                    int64
  ca_name       = models.CharField('Community area', max_length=100, null=True) # CA_name                  object
  place00       = models.CharField('???', max_length=100, null=True)            # Place00                  object
  gisdate       = models.CharField('???', max_length=100, null=True)            # GISDate                  object
  ptype         = models.IntegerField('Property type', null=True)               # PTYPE1_CAT                int64
  residential   = models.IntegerField('Residential?', null=True)                # RESIDENTIAL_PROPERTY      int64
  adj_yq        = models.IntegerField('Adjudicated quarter?', null=True)        # ADJ_YYYYQ                 int64
  adj_yd        = models.IntegerField('Adjudicated day?', null=True)            # ADJ_YYYYD                 int64

  loc           = models.PointField(null=True)
  objects       = models.GeoManager()

  def __unicode__(self):
    return unicode(self.pin)

# class PoliceBeat(models.Model):
#   district = models.IntegerField('District')
#   sector   = models.IntegerField('Sector')
#   beat     = models.IntegerField('Beat')
#   beat_num = models.IntegerField('Beat number')

#   mpoly    = models.MultiPolygonField()
#   objects  = models.GeoManager()

#   def __unicode__(self):
#     return self.beat_num

## class Crime(models.Model):
#   crimeid   = models.CharField('ID', max_length=20)
#   caseno    = models.CharField('Case Number', max_length=20)
#   timestamp = models.DateTimeField('Timestamp')
#   block     = models.CharField('Block', max_length=60)
#   iucr      = models.CharField('IUCR',max_length=10)
#   ptype     = models.CharField('Primary Type', max_length=100)
#   desc      = models.CharField('Description', max_length=100)
#   locdesc   = models.CharField('Location Description', max_length=100)
#   arrest    = models.BooleanField('Arrest')
#   domestic  = models.BooleanField('Domestic')
#   beat      = models.IntegerField('Beat number')
#   district  = models.IntegerField('District',null=True)
#   ward      = models.IntegerField('Ward',null=True)
#   comm_area = models.IntegerField('Community Area',null=True)
  
#   loc       = models.PointField(null=True)
#   objects   = models.GeoManager()

#   def __unicode__(self):
#     return self.crimeid

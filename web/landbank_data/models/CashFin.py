from django.contrib.gis.db import models

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


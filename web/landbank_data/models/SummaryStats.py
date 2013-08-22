from django.contrib.gis.db import models

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

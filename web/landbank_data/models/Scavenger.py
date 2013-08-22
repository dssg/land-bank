from django.contrib.gis.db import models

class Scavenger(models.Model):
  pin		= models.CharField('Property ID number', max_length=14, db_index=True)
  township	= models.IntegerField('Township (community area?) ID number', null=True)
  volume	= models.CharField('???', max_length=3, null=True)
  tax_year	= models.IntegerField('Year of tax balance', null=True)
  tax_type	= models.CharField('???', max_length=2, null=True)
  tax_amount	= models.FloatField('???', null=True)
  total_amount	= models.FloatField('???', null=True)
  def __unicode__(self):
    return unicode(self.pin)
  class Meta:
    app_label = 'landbank_data'

from django.contrib.gis.db import models

class IndicatorCache(models.Model):
  area_type	= models.CharField('municipality, ward, tract or community area',max_length=100)
  area_id	= models.IntegerField('Foreign key to the ward, censustract or communityarea table depending on area_type', null=True)
  indicator_name = models.CharField('indicator name', max_length=100)
  indicator_value = models.FloatField('indicator value')
  indicator_date = models.DateTimeField('date of indicator', null=True)
  def __unicode__(self):
    return unicode(self.area_type) + u' id:' + unicode(self.area_id)
  class Meta:
    app_label = 'landbank_data'

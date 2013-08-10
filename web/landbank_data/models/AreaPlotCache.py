from django.contrib.gis.db import models

class AreaPlotCache(models.Model):
  area_type	= models.CharField('ward, tract or community area',max_length=30, null=True)
  area_id	= models.IntegerField('Foreign key to the ward, censustract or communityarea table depending on area_type', null=True)
  json_str	= models.TextField('JSON string of data needed for charts/plots/graphs about this area', null=False, default='')
  def __unicode__(self):
    return unicode(self.area_type) + u' id:' + unicode(self.area_id)
  class Meta:
    app_label = 'landbank_data'

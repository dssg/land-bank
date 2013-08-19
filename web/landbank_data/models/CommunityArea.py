from django.contrib.gis.db import models

class CommunityArea(models.Model):
  area_number			= models.IntegerField('Community area number', null=True)
  area_name			= models.CharField('Community area name', max_length=80, null=True)
  shape_area			= models.FloatField('???', null=True)
  shape_len			= models.FloatField('???', null=True)
  geom				= models.MultiPolygonField(null=False, srid=3435)
  color_id                      = models.IntegerField('Map coloring index', null=True)
  objects			= models.GeoManager()
  def __unicode__(self):
    return unicode(self.area_number) + u'_' + unicode(self.area_name)
  class Meta:
    app_label = 'landbank_data'

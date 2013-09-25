from django.contrib.gis.db import models

class Municipality(models.Model):
  name		= models.CharField('Community area name', max_length=80, null=True)
  geom		= models.MultiPolygonField(null=False, srid=3435)
  color_id      = models.IntegerField('Map coloring index', null=True)
  objects	= models.GeoManager()
  def __unicode__(self):
    return unicode(self.name)
  class Meta:
    app_label = 'landbank_data'

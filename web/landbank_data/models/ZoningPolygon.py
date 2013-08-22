from django.contrib.gis.db import models

class ZoningPolygon(models.Model):
  zone_class = models.CharField('Zoning class', max_length=20)
  zone_type  = models.IntegerField('Zoning type')
  geom	     = models.MultiPolygonField(null=False, srid=3435)
  objects    = models.GeoManager()
  def __unicode__(self):
    return unicode(self.zone_class)
  class Meta:
    app_label = 'landbank_data'

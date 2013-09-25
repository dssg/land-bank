from django.contrib.gis.db import models

class CensusBlock(models.Model):
  fips 				= models.CharField('Census block identifying FIPS number', max_length=16)
  loc                           = models.MultiPolygonField(null=False, srid=3435)
  objects                       = models.GeoManager()
  def __unicode__(self):
    return unicode(self.fips)
  class Meta:
    app_label = 'landbank_data'

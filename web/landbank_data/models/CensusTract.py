from django.contrib.gis.db import models

class CensusTract(models.Model):
  fips 				= models.BigIntegerField('Census tract identifying FIPS number', null=True)
  loc                           = models.MultiPolygonField(null=False, srid=3435)
  color_id                      = models.IntegerField('Map coloring index', null=True)
  objects                       = models.GeoManager()
  def __unicode__(self):
    return unicode(self.fips)
  class Meta:
    app_label = 'landbank_data'

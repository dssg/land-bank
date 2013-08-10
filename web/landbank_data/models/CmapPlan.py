from django.contrib.gis.db import models

class CmapPlan(models.Model):
  name                          = models.CharField('CMAP LTA project name', max_length=200)
  status                        = models.CharField('Project status', max_length=50)
  study_area                    = models.CharField('Study area name', max_length=100)
  short_descr                   = models.CharField('Short description', max_length=100)
  url                           = models.CharField('Plan web site', max_length=200)
  loc                           = models.MultiPolygonField(null=False, srid=3435)
  objects                       = models.GeoManager()
  def __unicode__(self):
    return unicode(self.name)
  class Meta:
    app_label = 'landbank_data'

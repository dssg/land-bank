from django.contrib.gis.db import models

class BuildingPermit(models.Model):
  permit_number  = models.CharField('Permit Number', max_length=15, null=False)
  permit_type    = models.CharField('Crime ID', max_length=100)
  timestamp      = models.DateTimeField('Timestamp', null=True)
  cost           = models.FloatField('Cost')
  descr          = models.CharField('Description of work', max_length=200)
  pin            = models.CharField('PIN 1', max_length=20)
  loc            = models.PointField(null=True, srid=3435)
  objects	 = models.GeoManager()
  def __unicode__(self):
    return unicode(self.permit_number)
  class Meta:
    app_label = 'landbank_data'

from django.contrib.gis.db import models

class BusinessLicense(models.Model):
  license_number = models.CharField('License Number', max_length=15, null=False)
  legal_name     = models.CharField('Legal name', max_length=100)
  dba_name       = models.CharField('Doing business as name', max_length=100)
  timestamp      = models.DateTimeField('Expiration date', null=True)
  descr          = models.CharField('Description of license', max_length=200)
  code           = models.CharField('License code', max_length=40)
  loc            = models.PointField(null=True, srid=3435)
  objects	 = models.GeoManager()
  def __unicode__(self):
    return unicode(self.license_number)
  class Meta:
    app_label = 'landbank_data'

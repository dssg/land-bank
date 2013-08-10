from django.contrib.gis.db import models

class Brownfield(models.Model):
  # http://ofmpub.epa.gov/apex/cimc/f?p=100:55:0::NO:::
  pin            = models.CharField('Property ID number', max_length=14, null=True)
  recipient      = models.CharField('Cleanup recipient', max_length=100)
  agreementno    = models.CharField('EPA agreement number', max_length=50)
  granttype      = models.CharField('Type of brownfield grant', max_length=50)
  fundingtype    = models.CharField('Type of funding', max_length=50)
  acresid        = models.CharField('ACRES Property ID', max_length=50)
  loc            = models.PointField(null=True, srid=3435)
  objects	 = models.GeoManager()
  def __unicode__(self):
    return unicode(self.pin)
  class Meta:
    app_label = 'landbank_data'

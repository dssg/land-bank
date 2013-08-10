from django.contrib.gis.db import models

class CensusTractOccupancy(models.Model):
  fips                          = models.BigIntegerField('Census tract identifying FIPS number', null=True)
  owner_occ                     = models.IntegerField('Number of units occupied by owner', null=True)
  renter_occ                    = models.IntegerField('Number of units occupied by renters', null=True)
  def __unicode__(self):
    return unicode(self.fips)
  class Meta:
    app_label = 'landbank_data'

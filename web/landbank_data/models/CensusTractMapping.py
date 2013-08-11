from django.db import models
from Municipality import Municipality
from CommunityArea import CommunityArea
from Ward import Ward
from CensusTractCharacteristics import CensusTractCharacteristics
from CensusTractOccupancy import CensusTractOccupancy
from CensusTractIncome import CensusTractIncome

class CensusTractMapping(models.Model):
  fips                          = models.BigIntegerField('Census block identifying FIPS number', null=False)
  municipality			= models.ForeignKey(Municipality, null=True)
  municipality_frac		= models.FloatField(null=True)
  communityarea			= models.ForeignKey(CommunityArea, null=True)
  communityarea_frac		= models.FloatField(null=True)
  ward				= models.ForeignKey(Ward, null=True)
  ward_frac			= models.FloatField(null=True)
  characteristics               = models.ForeignKey(CensusTractCharacteristics, null=False)
  occupancy                     = models.ForeignKey(CensusTractOccupancy, null=False)
  income                        = models.ForeignKey(CensusTractIncome, null=False)
  def __unicode__(self):
    return unicode(self.fips)
  class Meta:
    app_label = 'landbank_data'

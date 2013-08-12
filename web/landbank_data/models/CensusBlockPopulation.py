from django.contrib.gis.db import models

class CensusBlockPopulation(models.Model):
  fips                          = models.BigIntegerField('Census block identifying FIPS number')
  pop				= models.IntegerField('Population')
  def __unicode__(self):
    return unicode(self.fips)
  class Meta:
    app_label = 'landbank_data'

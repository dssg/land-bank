from django.contrib.gis.db import models
from CensusBlock import CensusBlock

class CensusBlockEmployment(models.Model):
  # http://lehd.ces.census.gov/data/#lodes
  fips                          = models.BigIntegerField('Census block identifying FIPS number')
  censusblock                   = models.ForeignKey(CensusBlock, null=False)
  jobs				= models.IntegerField('Number of jobs')
  def __unicode__(self):
    return unicode(self.fips)
  class Meta:
    app_label = 'landbank_data'

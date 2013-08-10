from django.contrib.gis.db import models

class TractScores(models.Model):
  census_tract	= models.ForeignKey('CensusTract')
  stability	= models.IntegerField('Housing stability indicator based on Walker & Winston LISC paper', null=True)
  nuisance	= models.IntegerField('Nuisance score from 311, crime, etc.', null=True)
  affordability = models.IntegerField('Percent of tract population estimated to be able to afford median-priced SFH', null=True)
  impact	= models.IntegerField('Amount of impact property could have', null=True)
  vacancy       = models.IntegerField('Percentile among census tracts of estimated residential vacancy rate, via census data', null=True)
  def __unicode__(self):
    return unicode(self.census_tract)
  class Meta:
    app_label = 'landbank_data'


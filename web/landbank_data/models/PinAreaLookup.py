from django.contrib.gis.db import models

class PinAreaLookup(models.Model):
  pin		 = models.CharField('Property ID number', max_length=15, null=False, db_index=True)
  ward		 = models.ForeignKey('Ward',null=True)
  community_area = models.ForeignKey('CommunityArea',null=True)
  census_tract	 = models.ForeignKey('CensusTract',null=True)
  def __unicode__(self):
    return unicode(self.pin)
  class Meta:
    app_label = 'landbank_data'

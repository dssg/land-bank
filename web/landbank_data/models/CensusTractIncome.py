from django.contrib.gis.db import models

class CensusTractIncome(models.Model):
  fips				= models.BigIntegerField('Census tract identifying FIPS number', null=True)
  inc_lt_10			= models.FloatField('Percent of tract households earning <$10k annual gross', null=True)
  inc_10_15			= models.FloatField('Percent of tract households earning >=$10k and <$15k annual gross', null=True)
  inc_15_25			= models.FloatField('Percent of tract households earning >=$15k and <$25k annual gross', null=True)
  inc_25_35			= models.FloatField('Percent of tract households earning >=$25k and <$35k annual gross', null=True)
  inc_35_50			= models.FloatField('Percent of tract households earning >=$35k and <$50k annual gross', null=True)
  inc_50_75			= models.FloatField('Percent of tract households earning >=$50k and <$75k annual gross', null=True)
  inc_75_100			= models.FloatField('Percent of tract households earning >=$75k and <$100k annual gross', null=True)
  inc_100_150			= models.FloatField('Percent of tract households earning >=$100k and <$150k annual gross', null=True)
  inc_150_200			= models.FloatField('Percent of tract households earning >=$150k and <$200k annual gross', null=True)
  inc_gt_200			= models.FloatField('Percent of tract households earning >$200k annual gross', null=True)
  med_inc			= models.IntegerField('Median household annual gross income', null=True)
  med_house_txn_2011		= models.IntegerField('Median transaction amount for SF, condo and 2-4 fam homes in 2011', null=True)
  def __unicode__(self):
    return unicode(self.fips)
  class Meta:
    app_label = 'landbank_data'

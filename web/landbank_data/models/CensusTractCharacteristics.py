from django.contrib.gis.db import models

class CensusTractCharacteristics(models.Model):
  fips                          = models.BigIntegerField('Census tract identifying FIPS number') # 1
  pop                           = models.IntegerField('Total population') # 4
  median_age                    = models.FloatField('Median age', null=True) # 42
  pct_18plus                    = models.FloatField('Percentage 18 years of age and over', null=True) # 47
  pct_65plus                    = models.FloatField('Percentage 65 years of age and over', null=True) # 53
  pct_whitenh                   = models.FloatField('Percentage white Non-Hispanic', null=True) # 249
  pct_blacknh                   = models.FloatField('Percentage black Non-Hispanic', null=True) # 251
  pct_asiannh                   = models.FloatField('Percentage Asian Non-Hispanic', null=True) # 255
  pct_hispanic                  = models.FloatField('Percentage Hispanic', null=True) # 231
  housing_units                 = models.IntegerField('Total number of housing units') # 340
  pct_occ_units                 = models.FloatField('Percentage of occupied units',null=True) # 343
  pct_vac_units                 = models.FloatField('Percentage of vacant units',null=True) # 345
  pct_vac_owner                 = models.FloatField('Percentage of vacant non-rental units',null=True) # 359
  pct_vac_rental                = models.FloatField('Percentage of vacant rental units',null=True) # 361
  pct_owner_occupied            = models.FloatField('Percentage of owner occupied units', null=True) # 365
  owner_occ_hh_size             = models.FloatField('Average household size of owner occupied units', null=True) # 368
  pct_renter_occupied           = models.FloatField('Percentage of renter occupied units', null=True) # 371
  renter_occ_hh_size            = models.FloatField('Average household size of renter occupied units', null=True) # 374
  def __unicode__(self):
    return unicode(self.fips)
  class Meta:
    app_label = 'landbank_data'
  

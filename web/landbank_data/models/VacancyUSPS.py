from django.contrib.gis.db import models

class VacancyUSPS(models.Model):
  year          = models.IntegerField('Year')
  quarter       = models.IntegerField('Quarter')
  fips          = models.BigIntegerField('Census tract identifying FIPS number')
  naddr_res     = models.IntegerField('Total number of residential addresses')
  naddr_bus     = models.IntegerField('Total number of business addresses')
  naddr_oth     = models.IntegerField('Total number of other addresses')
  res_vacant    = models.IntegerField('Vacant residential addresses')
  bus_vacant    = models.IntegerField('Vacant business addresses')
  oth_vacant    = models.IntegerField('Vacant other addresses')
  res_vac_avg   = models.IntegerField('Average days residential address have been vacant')
  bus_vac_avg   = models.IntegerField('Average days business address have been vacant')
  res_vac_3     = models.IntegerField('Residential vacant 3 months or less')
  bus_vac_3     = models.IntegerField('Business vacant 3 months or less')
  oth_vac_3     = models.IntegerField('Other vacant 3 months or less')
  res_vac_3_6   = models.IntegerField('Residential vacant 3-6 months')
  bus_vac_3_6   = models.IntegerField('Business vacant 3-6 months')
  oth_vac_3_6   = models.IntegerField('Other vacant 3-6 months')
  res_vac_6_12  = models.IntegerField('Residential vacant 6-12 months')
  bus_vac_6_12  = models.IntegerField('Business vacant 6-12 months')
  oth_vac_6_12  = models.IntegerField('Other vacant 6-12 months')
  res_vac_12_24 = models.IntegerField('Residential vacant 12-24 months')
  bus_vac_12_24 = models.IntegerField('Business vacant 12-24 months')
  oth_vac_12_24 = models.IntegerField('Other vacant 12-24 months')
  res_vac_24_36 = models.IntegerField('Residential vacant 24-36 months')
  bus_vac_24_36 = models.IntegerField('Business vacant 24-36 months')
  oth_vac_24_36 = models.IntegerField('Other vacant 24-36 months')
  res_vac_36    = models.IntegerField('Residential vacant 36+ months')
  bus_vac_36    = models.IntegerField('Business vacant 36+ months')
  oth_vac_36    = models.IntegerField('Other vacant 36+ months')
  pqv_is_res    = models.IntegerField('Residential vacant previous quarter, now in use')
  pqv_is_bus    = models.IntegerField('Business vacant previous quarter, now in use')
  pqv_is_oth    = models.IntegerField('Other vacant previous quarter, now in use')
  pqv_ns_res    = models.IntegerField('Residential vacant previous quarter, now no-stat')
  pqv_ns_bus    = models.IntegerField('Business vacant previous quarter, now no-stat')
  pqv_ns_oth    = models.IntegerField('Other vacant previous quarter, now no-stat')
  res_nostat    = models.IntegerField('No-stat residential addresses')
  bus_nostat    = models.IntegerField('No-stat business addresses')
  oth_nostat    = models.IntegerField('No-stat other addresses')
  res_ns_3      = models.IntegerField('Residential no-stat 3 months or less')
  bus_ns_3      = models.IntegerField('Business no-stat 3 months or less')
  oth_ns_3      = models.IntegerField('Other no-stat 3 months or less')
  res_ns_3_6    = models.IntegerField('Residential no-stat 3-6 months')
  bus_ns_3_6    = models.IntegerField('Business no-stat 3-6 months')
  oth_ns_3_6    = models.IntegerField('Other no-stat 3-6 months')
  res_ns_6_12   = models.IntegerField('Residential no-stat 6-12 months')
  bus_ns_6_12   = models.IntegerField('Business no-stat 6-12 months')
  oth_ns_6_12   = models.IntegerField('Other no-stat 6-12 months')
  res_ns_12_24  = models.IntegerField('Residential no-stat 12-24 months')
  bus_ns_12_24  = models.IntegerField('Business no-stat 12-24 months')
  oth_ns_12_24  = models.IntegerField('Other no-stat 12-24 months')
  res_ns_24_36  = models.IntegerField('Residential no-stat 24-36 months')
  bus_ns_24_36  = models.IntegerField('Business no-stat 24-36 months')
  oth_ns_24_36  = models.IntegerField('Other no-stat 24-36 months')
  res_ns_36     = models.IntegerField('Residential no-stat 36+ months')
  bus_ns_36     = models.IntegerField('Business no-stat 36+ months')
  oth_ns_36     = models.IntegerField('Other no-stat 36+ months')
  pqns_is_res   = models.IntegerField('Residential no-stat previous quarter, now in use')
  pqns_is_bus   = models.IntegerField('Business no-stat previous quarter, now in use')
  pqns_is_oth   = models.IntegerField('Other no-stat previous quarter, now in use')
  def __unicode__(self):
    return unicode(self.fips)
  class Meta:
    app_label = 'landbank_data'

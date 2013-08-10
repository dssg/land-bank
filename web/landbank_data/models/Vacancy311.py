from django.contrib.gis.db import models

class Vacancy311(models.Model):
  request_no     = models.CharField('Request number', max_length=25)
  request_date   = models.DateTimeField('Request date')
  bldg_loc       = models.CharField('Building location', max_length=50)
  hazardous      = models.CharField('Hazardous condition?', max_length=50)
  boarded        = models.CharField('Boarded up?', max_length=50)
  entry_point    = models.CharField('Entry point', max_length=300)
  occupied       = models.CharField('Occupied?', max_length=300)
  fire           = models.NullBooleanField('Vacant due to fire')
  in_use         = models.NullBooleanField('In use?')
  houseno        = models.CharField('House number', max_length=10)
  direction      = models.CharField('Street direction', max_length=2)
  street         = models.CharField('Street name', max_length=100)
  suffix         = models.CharField('Street suffix', max_length=10)
  zipcode        = models.IntegerField('ZIP code')
  loc            = models.PointField(null=True,srid=3435)
  ward           = models.IntegerField('Ward')
  policedistrict = models.IntegerField('Police district')
  ca_num         = models.IntegerField('Community area number')
  latitude       = models.FloatField('Latitude')
  longitude      = models.FloatField('Longitude')
  objects        = models.GeoManager()
  def __unicode__(self):
    return unicode(self.request_no)
  class Meta:
    app_label = 'landbank_data'

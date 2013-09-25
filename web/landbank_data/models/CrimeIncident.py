from django.contrib.gis.db import models

class CrimeIncident(models.Model):
  crimeid        = models.CharField('Crime ID', max_length=15, null=False)
  caseno         = models.CharField('Crime ID', max_length=15)
  timestamp      = models.DateTimeField('Timestamp', null=False)
  block          = models.CharField('Block', max_length=100, null=False)
  iucr           = models.CharField('IUCR code', max_length=15, null=False)
  ptype          = models.CharField('Primary type', max_length=50, null=False)
  descr          = models.CharField('Description', max_length=100, null=False)
  locdescr       = models.CharField('Location description', max_length=100, null=False)
  arrest         = models.BooleanField('Arrest made?')
  domestic       = models.BooleanField('Domestic incident?')
  beat           = models.IntegerField('Beat number', null=False)
  district       = models.IntegerField('District number',null=True)
  ward           = models.IntegerField('Ward number',null=True)
  commarea       = models.IntegerField('Community Area number',null=True)
  fbicode        = models.CharField('FBI code', max_length=15, null=False)
  loc            = models.PointField(null=True, srid=3435)
  objects	 = models.GeoManager()
  def __unicode__(self):
    return unicode(self.crimeid)
  class Meta:
    app_label = 'landbank_data'

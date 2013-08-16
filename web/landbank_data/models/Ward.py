from django.contrib.gis.db import models

class Ward(models.Model):
  data_admin			= models.FloatField('???', null=True)
  perimeter			= models.FloatField('???', null=True)
  ward				= models.IntegerField('Ward number, does not match primary key', null=True)
  alderman			= models.CharField('Alderman name', max_length=60, null=True)
  ward_class			= models.IntegerField('???', null=True)
  ward_phone 			= models.CharField('Ward phone number', max_length=12, null=True)
  hall_phone			= models.CharField('???? phone number', max_length=12, null=True)
  hall_office			= models.CharField('???', max_length=45, null=True)
  address			= models.CharField('??? address', max_length=39, null=True)
  edit_date			= models.CharField('Unformatted date of last edit?', max_length=10, null=True)
  shape_area			= models.FloatField('???', null=True)
  shape_len			= models.FloatField('???', null=True)
  geom				= models.MultiPolygonField(null=False, srid=3435)
  color_id                      = models.IntegerField('Map coloring index', null=True)
  objects			= models.GeoManager()
  def __unicode__(self):
    return unicode(self.ward)
  class Meta:
    app_label = 'landbank_data'

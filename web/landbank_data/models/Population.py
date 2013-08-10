from django.db import models
class Population(models.Model):
  area_name			= models.CharField('Area name', max_length=100, null=True)
  area_type			= models.CharField('Area type', max_length=50, null=True)
  pop				= models.IntegerField('Population')
  def __unicode__(self):
    return unicode(self.area_name)
  class Meta:
    app_label = 'landbank_data'
    managed   = False
    db_table  = 'population'

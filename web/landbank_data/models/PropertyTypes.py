from django.contrib.gis.db import models

class PropertyTypes(models.Model):
  type_desc = models.CharField('Description of property type', max_length=30, null=True)

  def __unicode__(self):
    return unicode(self.type_desc)
  class Meta:
    app_label = 'landbank_data'

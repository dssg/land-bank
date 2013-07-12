from tastypie import fields
from landbank_data.models import Assessor
from tastypie.resources import ModelResource

class ParcelResource(ModelResource):
  class Meta:
    queryset = Assessor.objects.all()
    filtering = {
      "pin": ('exact'),
    }
    resource_name = 'parcel'

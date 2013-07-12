from tastypie import fields
from landbank_data.models import Assessor, Auction, CashFin, Foreclosure, Mortgage, Scavenger, Transaction
from tastypie.resources import ModelResource

class ParcelResource(ModelResource):
  class Meta:
    queryset = Assessor.objects.all()
    filtering = {
      "pin": ('exact'),
    }
    resource_name = 'parcel'

class AuctionResource(ModelResource):
  class Meta:
    queryset = Auction.objects.all()
    filtering = {
      "pin": ('exact'),
    }
    resource_name = 'auction'

class CashFinResource(ModelResource):
  class Meta:
    queryset = CashFin.objects.all()
    filtering = {
      "pin": ('exact'),
    }
    resource_name = 'cashfin'

class ForeclosureResource(ModelResource):
  class Meta:
    queryset = Foreclosure.objects.all()
    filtering = {
      "pin": ('exact'),
    }
    resource_name = 'foreclosure'

class MortgageResource(ModelResource):
  class Meta:
    queryset = Mortgage.objects.all()
    filtering = {
      "pin": ('exact'),
    }
    resource_name = 'mortgage'

class ScavengerResource(ModelResource):
  class Meta:
    queryset = Scavenger.objects.all()
    filtering = {
      "pin": ('exact'),
    }
    resource_name = 'scavenger'

class TransactionResource(ModelResource):
  class Meta:
    queryset = Mortgage.objects.all()
    filtering = {
      "pin": ('exact'),
    }
    resource_name = 'transaction'


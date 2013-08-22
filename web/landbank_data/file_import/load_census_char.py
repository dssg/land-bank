import os, csv
from models import CensusTractCharacteristics
from decimal import Decimal

census_file = '/mnt/ebs/data/DEC_10_SF1_SF1DP1/DEC_10_SF1_SF1DP1.csv'

def run(verbose = True):
  load_census(census_file, verbose = verbose)

def load_census(census_file, verbose = False):
  with open(census_file,'r') as f:
    reader = csv.reader(f, delimiter=",")
    reader.next()
    reader.next()
    skip_lookup = False
    if CensusTractCharacteristics.objects.count() == 0:
      skip_lookup = True
    for row in reader:
      fips               = '{:0>14}'.format(int(Decimal(row[1])))
      pop                = int(row[3])
      median_age         = float(row[41]) if row[41]!='' else None
      pct_18plus         = float(row[46]) if row[46]!='' else None
      pct_65plus         = float(row[52]) if row[52]!='' else None
      pct_whitenh        = float(row[248]) if row[248]!='' else None
      pct_blacknh        = float(row[250]) if row[250]!='' else None
      pct_asiannh        = float(row[254]) if row[254]!='' else None
      pct_hispanic       = float(row[230]) if row[230]!='' else None
      housing_units      = float(row[339]) if row[339]!='' else None
      pct_occ_units      = float(row[342]) if row[342]!='' else None
      pct_vac_units      = float(row[344]) if row[344]!='' else None
      pct_vac_owner      = float(row[358]) if row[358]!='' else None
      pct_vac_rental     = float(row[360]) if row[360]!='' else None
      pct_owner_occupied = float(row[364]) if row[364]!='' else None
      owner_occ_hh_size  = float(row[367]) if row[367]!='' else None
      pct_renter_occupied= float(row[370]) if row[370]!='' else None
      renter_occ_hh_size = float(row[373]) if row[373]!='' else None
      try:
        if skip_lookup:
          raise Exception('no lookup')
        tract = CensusTractCharacteristics.objects.get(\
          fips = fips)
      except:
        tract = CensusTractCharacteristics(\
          fips               = fips,\
          pop                = pop,\
          median_age         = median_age,\
          pct_18plus         = pct_18plus,\
          pct_65plus         = pct_65plus,\
          pct_whitenh        = pct_whitenh,\
          pct_blacknh        = pct_blacknh,\
          pct_asiannh        = pct_asiannh,\
          pct_hispanic       = pct_hispanic,\
          housing_units      = housing_units,\
          pct_occ_units      = pct_occ_units,\
          pct_vac_units      = pct_vac_units,\
          pct_vac_owner      = pct_vac_owner,\
          pct_vac_rental     = pct_vac_rental,\
          pct_owner_occupied = pct_owner_occupied,\
          owner_occ_hh_size  = owner_occ_hh_size,\
          pct_renter_occupied= pct_renter_occupied,\
          renter_occ_hh_size = renter_occ_hh_size\
        )
      tract.save()

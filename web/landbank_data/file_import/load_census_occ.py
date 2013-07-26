import os, csv
from models import CensusTractOccupancy
from decimal import Decimal

occupancy_file = '/mnt/ebs/data/DEC_10_SF1_SF1DP1/census_owner_rental_occupancy.csv'

def run(verbose = True):
  load_occupancy(occupancy_file, verbose = verbose)

def load_occupancy(occupancy_file, verbose = False):
  with open(occupancy_file,'r') as f:
    reader = csv.reader(f, delimiter=",")
    reader.next()
    reader.next()
    skip_lookup = False
    if CensusTractOccupancy.objects.count() == 0:
      skip_lookup = True
    #i = 0;
    for row in reader:
      #if (i==10):
        #break
      fips               = '{:0>14}'.format(int(Decimal(row[0])))
      try: owner_occ     = int(row[1])
      except: owner_occ = None
      try: renter_occ     = int(row[2])
      except: renter_occ = None
      try:
        if skip_lookup:
          raise Exception('no lookup')
        occupancy = CensusTractOccupancy.objects.get(\
          fips = fips\
          ,owner_occ = owner_occ\
          ,renter_occ = renter_occ\
        )
      except:
        occupancy = CensusTractOccupancy(\
          fips = fips\
          ,owner_occ = owner_occ\
          ,renter_occ = renter_occ\
        )
      #i += 1
      occupancy.save()

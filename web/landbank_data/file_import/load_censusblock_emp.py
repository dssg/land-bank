import os, csv
from models import CensusBlockEmployment, CensusBlock
from decimal import Decimal

census_file = '/mnt/ebs/data/il_wac_S000_JT00_2011.csv'

def run(verbose = True):
  load_census(census_file, verbose = verbose)

def load_census(census_file, verbose = False):
  with open(census_file,'r') as f:
    reader = csv.reader(f, delimiter=",")
    reader.next()
    skip_lookup = False
    if CensusBlockEmployment.objects.count() == 0:
      skip_lookup = True
    for row in reader:
      fips               = '{:0>15}'.format(int(Decimal(row[0])))
      block              = CensusBlock.objects.get(fips=fips)
      jobs               = int(row[1])
      try:
        if skip_lookup:
          raise Exception('no lookup')
        block = CensusBlockEmployment.objects.get(\
          fips = fips)
      except:
        block = CensusBlockEmployment(\
          fips               = fips               ,\
          censusblock        = block              ,\
          jobs               = jobs                \
        )
      block.save()

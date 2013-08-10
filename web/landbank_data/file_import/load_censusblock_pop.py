import os, csv
from models import CensusBlockPopulation
from decimal import Decimal

census_file = '/mnt/ebs/data/census/censusblockdata.2010/DEC_10_SF1_QTP6_with_ann.csv'

def run(verbose = True):
  load_census(census_file, verbose = verbose)

def load_census(census_file, verbose = False):
  with open(census_file,'r') as f:
    reader = csv.reader(f, delimiter=",")
    reader.next()
    reader.next()
    skip_lookup = False
    if CensusBlockPopulation.objects.count() == 0:
      skip_lookup = True
    for row in reader:
      fips               = '{:0>15}'.format(int(Decimal(row[1])))
      pop                = int(row[3])
      try:
        if skip_lookup:
          raise Exception('no lookup')
        block = CensusBlockPopulation.objects.get(\
          fips = fips)
      except:
        block = CensusBlockPopulation(\
          fips               = fips               ,\
          pop                = pop                 \
        )
      block.save()

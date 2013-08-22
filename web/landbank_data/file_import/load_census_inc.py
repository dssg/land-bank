import os, csv
from models import CensusTractIncome
from decimal import Decimal

income_file = '/mnt/ebs/data/aff_income/acs_household_inc.csv'

def run(verbose = True):
  load_income(income_file, verbose = verbose)

def load_income(income_file, verbose = False):
  with open(income_file,'r') as f:
    reader = csv.reader(f, delimiter=",")
    skip_lookup = False
    if CensusTractIncome.objects.count() == 0:
      skip_lookup = True
    for row in reader:
      fips		  = '{:0>14}'.format(int(Decimal(row[0])))
      try: inc_lt_10	  = float(row[1])
      except: inc_lt_10	  = None
      try: inc_10_15      = float(row[2])
      except: inc_10_15   = None 
      try: inc_15_25      = float(row[3])
      except: inc_15_25   = None 
      try: inc_25_35      = float(row[4])
      except: inc_25_35   = None 
      try: inc_35_50      = float(row[5])
      except: inc_35_50   = None 
      try: inc_50_75      = float(row[6])
      except: inc_50_75   = None 
      try: inc_75_100     = float(row[7])
      except: inc_75_100  = None 
      try: inc_100_150    = float(row[8])
      except: inc_100_150 = None 
      try: inc_150_200    = float(row[9])
      except: inc_150_200 = None 
      try: inc_gt_200     = float(row[10])
      except: inc_gt_200  = None 
      try: med_inc     	  = int(row[11])
      except: med_inc 	  = None
      try:
        if skip_lookup:
          raise Exception('no lookup')
        income = CensusTractIncome.objects.get(\
          fips         = fips,\
          inc_lt_10    = inc_lt_10,\
          inc_10_15    = inc_10_15,\
          inc_15_25    = inc_15_25,\
          inc_25_35    = inc_25_35,\
          inc_35_50    = inc_35_50,\
          inc_50_75    = inc_50_75,\
          inc_75_100   = inc_75_100,\
          inc_100_150  = inc_100_150,\
          inc_150_200  = inc_150_200,\
          inc_gt_200   = inc_gt_200 ,\
          med_inc      = med_inc\
        )
      except:
        income = CensusTractIncome(\
          fips 	       = fips,\
          inc_lt_10    = inc_lt_10,\
          inc_10_15    = inc_10_15,\
          inc_15_25    = inc_15_25,\
          inc_25_35    = inc_25_35,\
          inc_35_50    = inc_35_50,\
          inc_50_75    = inc_50_75,\
          inc_75_100   = inc_75_100,\
          inc_100_150  = inc_100_150,\
          inc_150_200  = inc_150_200,\
          inc_gt_200   = inc_gt_200 ,\
          med_inc      = med_inc\
        )
      income.save()

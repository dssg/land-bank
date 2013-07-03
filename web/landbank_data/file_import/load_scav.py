import os, csv
from load_utils import yy_to_yyyy
from models import Scavenger
from decimal import Decimal

scavenger_file = '/mnt/ebs/data/scavenger.tsv'

def run(verbose = True):
  load_scavengers(scavenger_file, verbose = verbose)

def load_scavengers(scavenger_file, verbose = False):
  with open(scavenger_file,'r') as f:
    reader = csv.reader(f, delimiter="\t")
    reader.next()
    #i = 0;
    for row in reader:
      #if (i==10):
        #break
      try:
        scavenger =  Scavenger.objects.get(\
	township = int(row[0])\
	,volume = row[1].strip()
	# We expect to see the format "01-23-456-789-0000' so we must strip hyphens
        ,pin = row[2].translate(None, '-').strip()\
	,tax_year = yy_to_yyyy(row[3])\
	,tax_type = row[4].strip()\
	,tax_amount = Decimal(row[5].translate(None, '$,'))\
	,total_amount = Decimal(row[6].translate(None, '$,'))\
        )
      except:
        scavenger =  Scavenger(\
	township = int(row[0])\
	,volume = row[1].strip()
	# We expect to see the format "01-23-456-789-0000' so we must strip hyphens
        ,pin = row[2].translate(None, '-').strip()\
	,tax_year = yy_to_yyyy(row[3])\
	,tax_type = row[4].strip()\
	,tax_amount = Decimal(row[5].translate(None, '$,'))\
	,total_amount = Decimal(row[6].translate(None, '$,'))\
        )
      #i += 1
      scavenger.save()

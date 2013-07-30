import os, csv
from models import LoanApplication

loanapplication_file = '/mnt/ebs/data/hmda/hmda_cook_09_11.csv'

def run(verbose = True):
  load_loanapplications(loanapplication_file, verbose = verbose)

def convert_3val_boolean(value):
  try: intval = int(value)
  except: intval = 2
  return False if intval is not 1 else True

def load_loanapplications(scavenger_file, verbose = False):
  with open(loanapplication_file,'r') as f:
    reader = csv.reader(f, delimiter=",")
    #reader.next() # no header in this file
    #i = 0;
    skip_lookup = False
    if LoanApplication.objects.count() == 0:
      skip_lookup = True

    for row in reader:
      #if (i==2):
        #break
      year			= int(row[0])
      respondent_id		= row[1].strip()
      agency_id			= int(row[2])
      loan_type			= int(row[3])
      property_type             = int(row[4])
      loan_purpose              = int(row[5])
      owner_occ		        = convert_3val_boolean(row[6])
      loan_amt                  = int(row[7]) * 1000
      preapproval_req           = convert_3val_boolean(row[8])
      action_type               = int(row[9])
      try:  fips                = long(row[11]+row[12]+row[13].replace(".",""))
      except: fips		= None
      try: applicant_income     = int(row[28]) * 1000
      except: applicant_income	= None
      purchaser_type            = int(row[29]) if int(row[29])>0 else None
      try: denial_reason1       = int(row[30]) if int(row[30])>0 else None
      except: denial_reason1	= None
      try: denial_reason2       = int(row[31]) if int(row[31])>0 else None
      except: denial_reason2	= None
      try: denial_reason3       = int(row[32]) if int(row[32])>0 else None
      except: denial_reason3	= None
      try: rate_spread          = float(row[33])
      except: rate_spread	= None
      try:  hoepa_status        = None if row[34] == '' else bool(2 - int(row[34]))
      except: hopea_status      = None
      try:  lien_status         = int(row[35]) if int(row[35])>0 else None
      except: lien_status       = None
      try:  population          = int(row[38]) if int(row[38])>0 else None
      except: population        = None
      try:  minority_pop_pct    = float(row[39])
      except: minority_pop_pct  = None
      try:  med_fam_inc         = int(row[40])
      except: med_fam_inc       = None
      try:  tract_msa_md_inc    = float(row[41])
      except: tract_msa_md_inc  = None
      try:  num_owner_occ       = int(row[42])
      except: num_owner_occ     = None
      try: num_1_4              = int(row[43])
      except: num_1_4           = None
      try:
        if skip_lookup:
          raise Exception('no lookup')
        loanapp = LoanApplication.objects.get(\
          year              = year\
          ,respondent_id     = respondent_id\
          ,agency_id         = agency_id\
          ,loan_type         = loan_type\
          ,property_type     = property_type\
          ,loan_purpose      = loan_purpose\
          ,owner_occ         = owner_occ\
          ,loan_amt          = loan_amt\
          ,preapproval_req   = preapproval_req\
          ,action_type       = action_type\
          ,fips              = fips\
          ,applicant_income  = applicant_income\
          ,purchaser_type    = purchaser_type\
          ,denial_reason1    = denial_reason1\
          ,denial_reason2    = denial_reason2\
          ,denial_reason3    = denial_reason3\
          ,rate_spread       = rate_spread\
          ,hoepa_status      = hoepa_status\
          ,lien_status       = lien_status\
          ,population        = population\
          ,minority_pop_pct  = minority_pop_pct\
          ,med_fam_inc       = med_fam_inc\
          ,tract_msa_md_inc  = tract_msa_md_inc\
          ,num_owner_occ     = num_owner_occ\
          ,num_1_4           = num_1_4\
        )
      except:
        loanapp = LoanApplication(\
          year              = year\
          ,respondent_id     = respondent_id\
          ,agency_id         = agency_id\
          ,loan_type         = loan_type\
          ,property_type     = property_type\
          ,loan_purpose      = loan_purpose\
          ,owner_occ         = owner_occ\
          ,loan_amt          = loan_amt\
          ,preapproval_req   = preapproval_req\
          ,action_type       = action_type\
          ,fips              = fips\
          ,applicant_income  = applicant_income\
          ,purchaser_type    = purchaser_type\
          ,denial_reason1    = denial_reason1\
          ,denial_reason2    = denial_reason2\
          ,denial_reason3    = denial_reason3\
          ,rate_spread       = rate_spread\
          ,hoepa_status      = hoepa_status\
          ,lien_status       = lien_status\
          ,population        = population\
          ,minority_pop_pct  = minority_pop_pct\
          ,med_fam_inc       = med_fam_inc\
          ,tract_msa_md_inc  = tract_msa_md_inc\
          ,num_owner_occ     = num_owner_occ\
          ,num_1_4           = num_1_4\
      )
      #i += 1
      loanapp.save()

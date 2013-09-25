from django.contrib.gis.db import models

class LoanApplication(models.Model):
  year              = models.IntegerField('2009, 2010, 2011', null=True)
  respondent_id     = models.CharField('10 character identifier', max_length=10, null=True)
  agency_id         = models.IntegerField('OCC, FRS, FDIC, N/A, NCUA, N/A, HUD, N/A, CFPB', null=True)
  loan_type         = models.IntegerField('Conventional, FHA-insured, VA-guaranteed, FSA/RHS', max_length=12, null=True)
  property_type     = models.IntegerField('1-4 family, Manufactured, multifamily', null=True)
  loan_purpose      = models.IntegerField('Purchase, improvement, refinancing', null=True)
  owner_occ         = models.NullBooleanField('Whether property is owner-occupied, if applicable', null=True)
  loan_amt          = models.IntegerField('Dollar amount of loan', null=True) # in thousands, with leading 0s
  preapproval_req   = models.NullBooleanField('Whether pre-approval was requested, if applicable', null=True)
  action_type       = models.IntegerField('Originated, not accepted, denied, withdrawn, incomplete, purchased, preapproval denied, preapproval not accepted', null=True)
  fips              = models.BigIntegerField('Full 11-digit FIPS census tract code with implied decimal point between 2nd and 3rd last digits', null=True) #tract_id (all in format '####.##')
  applicant_income  = models.IntegerField('Gross annual applicant income', null=True) # in thousands, with leading 0s
  purchaser_type    = models.IntegerField('Fannie, Ginnie, Freddie, Farmer, private, commercial bank, life ins/credit union/mortgage bank/finance co., affiliate inst., other; null implies loan not originated or not sold in this calendar year', null=True)
  denial_reason1    = models.IntegerField('Debt-to-income ratio, employment, credit, collateral, insuff. cash, unverifiable info, incomplete credit application, mort ins denied, other', null=True)
  denial_reason2    = models.IntegerField('Debt-to-income ratio, employment, credit, collateral, insuff. cash, unverifiable info, incomplete credit application, mort ins denied, other', null=True)
  denial_reason3    = models.IntegerField('Debt-to-income ratio, employment, credit, collateral, insuff. cash, unverifiable info, incomplete credit application, mort ins denied, other', null=True)
  rate_spread       = models.FloatField('Percent above APR of mortgage rate', null=True) # has leading 0s
  hoepa_status      = models.NullBooleanField('Whether it\'s a HOEPA loan, only for loans originated or purchased', null=True)   # may have NA values
  lien_status       = models.IntegerField('Secured by 1st lien, secured by subordinate lien, not secured, null implies N/A or loan was purchased', null=True) #
  population        = models.IntegerField('Total population in tract', null=True) # has leading 0s and NAs 
  minority_pop_pct  = models.FloatField('Percentage of minority population to total population for tract', null=True) # has leading 0s and NAs
  med_fam_inc       = models.IntegerField('HUD median family income in dollars for the MSA/MD in which the tract is located, adjusted annually by HUD', null=True)
  tract_msa_md_inc  = models.FloatField('Percent of tract median family income compared to MSA/MD median family income', null=True) # has NAs
  num_owner_occ     = models.IntegerField('Number of dwellings, including individual condos, that are lived in by the owner', null=True) # has leading 0s and NAs
  num_1_4           = models.IntegerField('Dwellings that are built to house fewer than 5 families', null=True)  # has leading 0s and NAs
  def __unicode__(self):
    return unicode(self.fips) + u' ' + unicode(self.loan_amt)
  class Meta:
    app_label = 'landbank_data'

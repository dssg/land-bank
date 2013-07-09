#!/usr/bin/env python
# Demonstrate some simple land bank analytics tools
from landbank_data.models import Assessor, Foreclosure, Transaction, CensusTract
import pylab as py
import sys, datetime

def get_tract(prop):
  tracts = CensusTract.objects.filter(\
    loc__contains=(prop.loc))
  assert len(tracts) == 1
  print tracts[0].geoid
  return tracts[0]

def get_tract_assessments(prop, sametype=True):
  ''' Get the assessed value of all units within the same tract of
      a given property. If sametype=True, restrict to properties
      of the same type (SFH, condo, etc.) '''

  tract = get_tract(prop)

  # Filter assessment table based on distance
  nearby = Assessor.objects.filter(\
    loc__contained=(tract.loc)).filter(\
    no_tract_info__exact=False)

  # Optionally filter based on property type.
  if sametype:
    nearby = nearby.filter(ptype__exact=prop.ptype)

  # Return the list of properties.
  return nearby

def get_tract_hunits(prop, sametype=True):

  return len(get_tract_assessments(prop, sametype=sametype))


def get_tract_foreclosures(prop):
  ''' Get all foreclosures within the same tract of a given property.'''

  tract = get_tract(prop)

  # Filter foreclosure table based on distance.
  nearby = Foreclosure.objects.filter(\
    loc__contained=(tract.loc)).filter(\
    no_tract_info__exact=False)

  # Return the list of properties
  return nearby


def get_tract_transactions(prop, sametype=True):
  ''' Get all real estate transactions within the same tract of 
      a given property. If sametype=True, restrict to properties
      of the same type (SFH, condo, etc.) '''

  tract = get_tract(prop)

  # Filter the transaction table based on distance
  nearby = Transaction.objects.filter(\
    loc__contained=(tract.loc)).filter(\
    no_tract_info__exact=False)

  # Optionally filter based on property type
  if sametype:
    nearby = nearby.filter(ptype__exact=prop.pt_type1_cat)

  # Return the list of properties
  return nearby


#####################################################################################
# If this program is called from the command line with an argument of a pin or
# an address, give a summary of the local real estate market.
# If you pass in a pin, make sure it's 14 digits and valid.
# If you pass in an address, include the street number, direction, and name.
#   A single unit of a multi-unit address will be chosen arbitrarily.
#####################################################################################

if __name__ == '__main__':
  # First pick out the property based on the command line arguments.
  myprop = None
  # Single argument is treated as a PIN.
  if len(sys.argv) == 2:
    myprop=Assessor.objects.get(pin = int(sys.argv[1]))
  # Multiple arguments are treated as an address.
  else:
    myprop=Assessor.objects.filter(\
      houseno   = sys.argv[1].upper(),\
      direction = sys.argv[2].upper(),\
      street    = sys.argv[3].upper())[0]

  # Get assessed values of tract properties.
  assmt_props = get_tract_assessments(myprop)
  # Unpack the values from the list.
  assmts = [i.current_total_assmt for i in assmt_props if i.current_total_assmt is not None]

  # Plot the results.
  py.hist(assmts, bins=20)
  py.plot([myprop.current_total_assmt,myprop.current_total_assmt],\
          py.ylim(),'r-')
  py.xlabel('Assessed value')
  py.ylabel('Number of properties')
  py.title('Nearby assessments of similar properties')
  py.savefig('assessment_hist.png')

  # Now do foreclosures.
  print ' '
  print 'Foreclosures'
  print '------------'
  # Get foreclosures from tract properties.
  forec_props = get_tract_foreclosures(myprop)

  # List them sorted by date.
  forec_2012 = 0
  for i in sorted(forec_props,key=lambda j: j.filing_date):
    if i.filing_date.year == 2012: 
      forec_2012=forec_2012+1
      print '%10s -- %10s %2s %20s %10s' % \
        (datetime.datetime.strftime(i.filing_date, '%m/%d/%Y'),\
        i.houseno, i.direction, i.street, i.apt)

  print '----'
  print '%d foreclosures out of %d similar units in 2012' % (forec_2012,\
    get_tract_hunits(myprop))
  print '----'

  # Finally, let's do transactions.
  print ' '
  print 'Transactions'
  print '------------'
  # As before, get the tract transactions.
  trans_props = get_tract_transactions(myprop)

  # Display them sorted by date...
  trans_2012 = 0
  busbuy_2012 = 0
  for i in sorted(trans_props,key=lambda j: j.date_rec):
    if i.date_rec.year == 2012: 
      trans_2012=trans_2012+1
      if i.business_buyer: busbuy_2012 = busbuy_2012+1
      print '%10s -- %10s %2s %20s %10s %10.2f' % \
        (datetime.datetime.strftime(i.date_rec, '%m/%d/%Y'),\
        i.houseno, i.direction, i.street, i.apt, i.amount_prime)

  print '----'
  print '%d transactions out of %d similar units in 2012' % (trans_2012,\
    get_tract_hunits(myprop))
  print '%d were business buyers' % (busbuy_2012,)
  print '----'

  # And plot the amount versus time.
  py.clf()
  py.plot([i.date_rec for i in trans_props],\
          [i.amount_prime for i in trans_props],\
          '.')
  py.xlabel('Date of sale')
  py.ylabel('Sale amount')
  py.title('Nearby sales of similar properties')
  py.savefig('nearby_sales.png')

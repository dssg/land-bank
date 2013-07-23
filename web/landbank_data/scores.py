from models import CrimeIncident, Assessor, Vacancy311
import datetime
import csv
from pytz import timezone

cst = timezone('US/Central')

def nuisance(pin, radius_ft=200.0, time_yr=1.0):
  retval = 0

  thisprop = Assessor.objects.get(pin=pin)

  crimes = CrimeIncident.objects.filter(\
    loc__dwithin=(thisprop.loc, radius_ft)).filter(\
    timestamp__gte=(cst.localize(datetime.datetime.now() - \
                    datetime.timedelta(days=time_yr*365.25))))

  for crime in crimes:
    if   crime.ptype in ['HOMICIDE']: retval += 10
    elif crime.ptype in ['CRIM SEXUAL AS', 'WEAPONS VIOLAT']: retval += 5
    elif crime.ptype in ['ARSON','BURGLARY']: retval += 3
    elif crime.ptype in ['PROSTITUTION','NARCOTICS']: retval += 1
    else: pass

  complaints = Vacancy311.objects.filter(\
    loc__dwithin=(thisprop.loc, radius_ft)).filter(\
    request_date__gte=(cst.localize(datetime.datetime.now() - \
                       datetime.timedelta(days=time_yr*365.25))))

  for complaint in complaints:
    retval += 1

  return retval


def test_nuisance_score():
  with open('/home/tplagge/nuisance_mc.csv','w') as f:
    csvwriter = csv.writer(f)
    myparcels = Assessor.objects.filter(long_x__isnull=False).filter(place__exact=('Chicago')).order_by('?')[:10000]
    for parcel in myparcels:
      row = [parcel.long_x, parcel.lat_y, nuisance(parcel.pin)]
      csvwriter.writerow(row)

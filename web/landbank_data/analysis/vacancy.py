from models import VacancyUSPS, TractScores, CensusTract
from numpy import asscalar
import scipy

# Run this to populate the "vacancy percentile" for each census tract
vac = VacancyUSPS.objects.filter(year__exact=2012).filter(quarter__exact=4)
vals = vac.values('fips','naddr_res','res_vacant')
vac_pcts = []
fips_vac_pct = {}

for v in vals:
  my_fips = str(v['fips'])
  fips_vac_pct[my_fips] = {}
  if v['naddr_res']:
    pct = float(v['res_vacant']) / float(v['naddr_res'])
    vac_pcts.append(pct)
    fips_vac_pct[my_fips]['vac_pct'] = pct
  else:
    vac_pcts.append(0)
    fips_vac_pct[my_fips]['vac_pct'] = 0

for k,v in fips_vac_pct.iteritems():
  ct = CensusTract.objects.get(fips=k)
  ts = TractScores.objects.get(census_tract_id=ct.id)
  vac_pctl = asscalar(scipy.stats.percentileofscore(vac_pcts,v['vac_pct']))
  ts.vacancy = vac_pctl
  ts.save()
  print 'saved FIPS# ' + k + ' vacancy percentile to ' + str(vac_pctl)


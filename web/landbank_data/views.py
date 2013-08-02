from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from landbank_data.models import Assessor, PinAreaLookup, CommunityAreas, CensusTract, Wards, Transaction, TractScores
import datetime
import numpy as np
from pytz import timezone
import json

def pin(request, search_pin=None):
    try:		          search_assessor = Assessor.objects.get(pin=search_pin)
    except Assessor.DoesNotExist: search_assessor = None
    else:		          lookup = PinAreaLookup.objects.get(pin=search_pin)

    try:      ward = Wards.objects.get(pk=lookup.ward_id)
    except:   ward = None

    try:      ca = CommunityAreas.objects.get(pk=lookup.community_area_id)
    except:   ca = None

    try:      tract = CensusTract.objects.get(pk=lookup.census_tract_id)
    except:   tract = None

    try:      score = TractScores.objects.get(census_tract_id=lookup.census_tract_id)
    except:   score = None

    return render(request, 'landbank_data/pin.html', {\
	 'assessor': search_assessor\
	,'ward': ward\
	,'ca': ca\
	,'tract': tract\
	,'score': score\
	})

def commarea(request, search_commarea=None):
  cas = [i.area_number for i in CommunityAreas.objects.all()]
  sfhs = []
  cst = timezone('US/Central')
  oneyearago = cst.localize(datetime.datetime.now() - \
                            datetime.timedelta(days=365))

  #for ica, ca in enumerate(cas):
  #  # Only do the first ten because it's slow!
  #  if ica==10: break
  #  sfhs.append(np.median([i.amount_prime for i in \
  #    Transaction.objects.filter(ca_num__exact=ca).\
  #    filter(date_doc__lte=oneyearago).filter(ptype=1)]))
  bins = [ 1.07497143,
           1.23947429,
           1.40397714,
           1.56848,
           1.73298286,
           1.89748571,
           2.06198857,
           2.22649143,
           2.39099429,
           2.55549714,
           2.72]
  #sfh_vals, bins = np.histogram(sfhs,bins=mybins)
  sfh_vals = [1,
              0,
              1513,
              1215,
              0,
              0,
              0,
              0,
              0,
              427]
  data = []
  for b,v in zip(bins,sfh_vals):
    data.append({'x':b, 'y':v})

  print data
  return render_to_response('commarea2.html', {'data': json.dumps(data)},\
                            context_instance=RequestContext(request))


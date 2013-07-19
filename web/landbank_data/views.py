from django.shortcuts import render, get_object_or_404
from landbank_data.models import Assessor, PinAreaLookup, CommunityAreas, CensusTract, Wards

def pin(request, search_pin=None):
#    search_assessor = get_object_or_404(Assessor, pin=search_pin)
    try:
        search_assessor = Assessor.objects.get(pin=search_pin)
    except Assessor.DoesNotExist:
        search_assessor = None
    else:
        lookup = PinAreaLookup.objects.get(pin=search_pin)

    try:
        ward = Wards.objects.get(pk=lookup.ward_id)
    except:
        ward = None
    try:
        ca = CommunityAreas.objects.get(pk=lookup.community_area_id)
    except:
        ca = None
    try:
        tract = CensusTract.objects.get(pk=lookup.census_tract_id)
    except:
        tract = None

    return render(request, 'landbank_data/pin.html', {'assessor': search_assessor, 'ward': ward, 'ca': ca, 'tract': tract})


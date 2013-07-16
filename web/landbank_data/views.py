from django.shortcuts import render, get_object_or_404
from landbank_data.models import Assessor

def pin(request, search_pin=None):
#    search_assessor = get_object_or_404(Assessor, pin=search_pin)
    try:
        search_assessor = Assessor.objects.get(pin=search_pin)
    except Assessor.DoesNotExist:
        search_assessor = None
    return render(request, 'landbank_data/pin.html', {'assessor': search_assessor})


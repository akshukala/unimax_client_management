from django.db.models import Q
from uni_db.client_erp.models import BillingAddress

REGISTRY = {}


def register(kind):
    '''This decorator returns the function of the particular field '''
    def registrar(function):
        REGISTRY[kind] = function
        return function
    return registrar


@register("area")
def ac_state(data):
    query = data.get("term", None)

    if query:
        areas = BillingAddress.objects.filter(
            area__istartswith=query).values_list('area', flat=True).distinct()
    else:
        areas = []

    return list(set(areas))


def handle_request(kind, data):
    ''' This method is called to update form field with field and new \
    data returns a function to update that particular field'''
    return REGISTRY.get(kind)(data)
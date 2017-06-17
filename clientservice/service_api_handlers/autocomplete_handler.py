from django.db.models import Q
from uni_db.client_erp.models import BillingAddress
from uni_db.order_management.models import Order

REGISTRY = {}


def register(kind):
    '''This decorator returns the function of the particular field '''
    def registrar(function):
        REGISTRY[kind] = function
        return function
    return registrar


@register("area")
def ac_area(data):
    query = data.get("term", None)

    if query:
        areas = BillingAddress.objects.filter(
            area__istartswith=query).values_list('area', flat=True).distinct()
    else:
        areas = []

    return list(set(areas))


@register("order")
def ac_order(data):
    query = data.get("term", None)
    response = []
    if query:
        try:
            orders = Order.objects.filter(sales_order_id=query)
            response = [{
                "SalesOrderId ": str(order.sales_order_id),
                "value": order.sales_order_id,
                "status": order.status,
                } for order in orders]
        except ValueError:
            pass
    return response


def handle_request(kind, data):
    ''' This method is called to update form field with field and new \
    data returns a function to update that particular field'''
    return REGISTRY.get(kind)(data)
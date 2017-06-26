from flask.globals import request
from clientservice.utils.resource import Resource
from uni_db.client_erp.models import ShippingAddress


class RelatedClients(Resource):

    def get(self):
        related_clients = ShippingAddress.objects.filter(area=str(request.args.get('area')))[:7]
        client_data = {}
        if len(related_clients) <= 5 and len(related_clients) >= 0:
            client_data['clients'] = [{
                                     'client_id': str(cl.client.client_id),
                                     'name': str((cl.client.client_name
                                                  ).title()),
                                     }for cl in related_clients]
        else:
            client_data['clients'] = "Not Available"
        return client_data

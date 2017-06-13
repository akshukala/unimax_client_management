import json

from flask import current_app as app
from flask import request
from clientservice.utils.resource import Resource
from clientservice.service_api_handlers import get_client_details_handler


class ClientDetails(Resource):

    def get(self):
        """
           This method is used to fetch farmer(s) details
           for the farmer's details provided
        """
        request_data = request.args.to_dict()
        app.logger.info("Received Farmer Details get request")
        app.logger.info(json.dumps(request_data))

        if "farmer_id" in request_data:
#             return get_client_details_handler.get_farmer_datails(request_data)
            return "Success"
        elif "search_type" in request_data:
            return get_client_details_handler.search_client_details(request_data)

        return {
            'errorCode': 503,
            'errorMessage': "Parameters not found"
        }

#     def put(self):
#         app.logger.debug('Received farmer update request: %s',
#                          request.json)
#         return put_farmer_details_handler.handle_request(request.json)
# 
#     def post(self):
#         app.logger.debug(request.__dict__)
#         app.logger.debug('Received farmer creation request: %s',
#                          request.json)
#         return post_farmer_details_handler.handle_request(request.json)

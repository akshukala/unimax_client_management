from flask import current_app as app
from clientservice.utils.resource import Resource
from clientservice.service_api_handlers import (
    get_csr_details_handler,
)


class CSRDetails(Resource):

    def get(self):
        """
           This method is used to fetch Customer details
        """
        app.logger.info("Received CSR Details get request")

        return get_csr_details_handler.handle_request()
from flask import Flask, request
from flask import current_app as app

#from clientserviceservice.conf.config_logger_setup import setup_config_logger
from clientservice.service_api_handlers import autocomplete_handler
from clientservice.utils.resource import Resource


class Autocomplete(Resource):
    def get(self):
        app.logger.debug("Received Autocomplete Request")
        request_data = request.args.to_dict()
        return autocomplete_handler.handle_request(
            request_data.get("type", ""),
            request_data
        )
    get.authenticated = False

# if __name__ == '__main__':
#     test_app = Flask(__name__)
#     test_api = restful.Api(test_app)
#     setup_config_logger(test_app)
#     test_api.add_resource(Autocomplete, '/autocomplete/')
#     test_app.run()
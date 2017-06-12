from clientservice.utils.resource import Resource
class Ping(Resource):

    def get(self):
        """
           This method is used to fetch Customer details
        """

        return {"success": True}
    get.authenticated = False

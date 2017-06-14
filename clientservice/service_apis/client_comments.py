from flask import current_app as app
from flask import request
from clientservice.utils.resource import Resource
from uni_db.client_erp.models import Client, ClientComment
from clientservice.utils.auth import get_user


class ClientComments(Resource):

    def post(self):
        """
           This method is used to post client comment
        """
        app.logger.info("Received Client Comments Post Request")

        data = request.get_json(force=True)
        client_id = data.get('client_id')
        comment = data.get('comment')

        if not client_id or not comment:
            return {
                'responseCode': 503,
                'Message': "Parameters not found"
            }

        try:
            Customer = get_user()
            ClientComment.objects.create(
                client=Client.objects.get(client_id=client_id),
                comment=comment,
                commented_by=Customer
            )
            return {
                "success": True,
                "status": 200
            }
        except Exception as e:
            app.logger.debug(str(e))
            return {
                "success": False,
                "status": 200
            }
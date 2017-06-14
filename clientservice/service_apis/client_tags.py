from flask import request
from clientservice.utils.resource import Resource
from uni_db.client_erp.models import Tags, AddCall, Client, CallTag
from clientservice.utils.auth import get_user


class ClientTags(Resource):

    def get(self):
        '''Get all orders whose status is returnes'''
        tags = Tags.objects.all()
        return [{"tag_name": tag.tag_name,
                 "id": tag.id,
                "description": tag.tag_description} for tag in tags]

    def post(self):
        request_data = request.get_json(force=True)
        tags = request_data.get('tags')
        client_id = int(request_data.get('client_id'))
        add_call_obj = AddCall.objects.create(client=Client.objects.get(client_id=client_id),
                                              created_by=get_user())
        tag_count = len(tags)
        Client.objects.filter(client_id=client_id).update(modified_by=get_user())
        for i in range(0, tag_count):
            CallTag.objects.create(call=add_call_obj, tags=tags[i])
        return 'Tags Successfully Added'
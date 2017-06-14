import requests
from flask import request
from clientservice.utils.resource import Resource
from uni_db.client_erp.models import ClientMobile


class UniBankDetails(Resource):
    def get(self):
        mobile_no = ClientMobile.objects.filter(client__client_id=int(request.args.get('client_id')))[0].mobile
        message = """1. HDFC Bank Ac Name- Krishi Ex (BHANDARKAR ROAD BRANCH)
         Ac No- 50200017874993 IFSC Code - HDFC0000007 2.Bank of Maharashtra Ac
          Name- Krishi Ex (Deccan Gymkhana BRANCH) Ac No- 60246883147 IFSC
          Code - MAHB0000003"""
#         url = "http://sms.domainadda.com/vendorsms/pushsms.aspx?user=krishiex&password=krishiex@123&msisdn=91"+mobile_no+"&sid=KRISHI&msg="+message+"&fl=0&gwid=2"
#         requests.get(url)
        return {"responseCode": 200,
                "Message": "Bank Details Sent Successfully"}
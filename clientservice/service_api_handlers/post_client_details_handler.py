from uni_db.client_erp.models import (Client, BillingAddress,
                                      ShippingAddress, ClientMobile,
                                      ClientWhatsapp, ClientLandline)

from clientservice.utils.auth import get_user
from flask import current_app as app


def handle_request(data):
    try:
        c = Client(client_name=data.get('client_name'),
                   entered_by=get_user(),
                   modified_by=get_user()
                   )
        contact = data['contactInformation']
        mobile = contact['mobile']
        whatsapp = contact['whatsapp']
        landline = contact['landline']
        c.save()
        if len(mobile) > 0:
            for mob in mobile:
                ClientMobile.objects.create(mobile=str(mob), client=c)
        if len(whatsapp) > 0:
            for wt in whatsapp:
                ClientWhatsapp.objects.create(whatsapp=str(wt), client=c)
        if len(landline) > 0:
            for ll in landline:
                ClientLandline.objects.create(landline=str(ll), client=c)
    except Exception as e:
        app.logger.debug(str(e))
        return {
            "responseCode": 503,
            "Message": "Error creating farmer profile"
        }

    try:
        baddress = BillingAddress.objects.create(
            client=c,
            state=data.get('state'),
            city=data.get('city'),
            address_line1=data.get('address_line1'),
            area=data.get('area'),
            pin_code=data.get('pin_code'),
            country="India"
        )

        saddress = ShippingAddress.objects.create(
            client=c,
            state=data.get('state'),
            city=data.get('city'),
            address_line1=data.get('address_line1'),
            area=data.get('area'),
            pin_code=data.get('pin_code'),
            country="India"
        )
        c.billing_addressid = baddress.id
        c.shipping_addressid = saddress.id
        c.save()
    except Exception as e:
        app.logger.debug(str(e))
        return {
            "responseCode": 503,
            "Message": "Error in saving farmer address"
        }
    return {
        "client_id": c.client_id
    }
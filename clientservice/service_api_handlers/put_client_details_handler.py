from uni_db.client_erp.models import (Client, BillingAddress,
                                      ShippingAddress, ClientMobile,
                                      ClientWhatsapp, ClientLandline)
from flask import current_app as app


def handle_request(data):
    try:
        client_id = data.get('client_id', '').strip('/')
        client = Client.objects.get(client_id=client_id)
        return update_basic_details(client, data)

    except Client.DoesNotExist:
        return "ClientNotFound"


def update_basic_details(client, data):
    app.logger.debug("Updating Basic Information")
    try:
        client.client_name = data.get('client_name')
        contact = data['contactInformation']
        mobile = contact['mobile']
        whatsapp = contact['whatsapp']
        landline = contact['landline']

        mobile_objs = ClientMobile.objects.filter(client=client)
        if len(mobile_objs) == len(mobile):
                for i, mob in enumerate(mobile):
                    mobile_objs[i].mobile = str(mob)
                    mobile_objs[i].save()
        else:
                if len(mobile_objs) < len(mobile):
                    for mob in mobile:
                        if ClientMobile.objects.filter(client=client,
                                                       mobile=str(mob)).exists():
                            continue
                        else:
                            ClientMobile.objects.get_or_create(client=client,
                                                               mobile=str(mob))
                else:
                    mobile_objs.delete()
                    if len(mobile) > 0:
                        for mob in mobile:
                            ClientMobile.objects.create(mobile=str(mob),
                                                        client=client)

        whatsapp_objs = ClientWhatsapp.objects.filter(client=client)
        if len(whatsapp_objs) == len(whatsapp):
                for i, wapp in enumerate(whatsapp):
                    whatsapp_objs[i].whatsapp = str(wapp)
                    whatsapp_objs[i].save()
        else:
                if len(whatsapp_objs) < len(whatsapp):
                    for wapp in whatsapp:
                        if ClientWhatsapp.objects.filter(client=client,
                                                         whatsapp=str(wapp)).exists():
                            continue
                        else:
                            ClientWhatsapp.objects.get_or_create(client=client,
                                                                 whatsapp=str(wapp))
                else:
                    whatsapp_objs.delete()
                    if len(whatsapp) > 0:
                        for wapp in whatsapp:
                            ClientWhatsapp.objects.create(whatsapp=str(wapp),
                                                          client=client)

        landline_objs = ClientLandline.objects.filter(client=client)
        if len(landline_objs) == len(landline):
                for i, ll in enumerate(landline):
                    landline_objs[i].landline = str(ll)
                    landline_objs[i].save()
        else:
                if len(landline_objs) < len(landline):
                    for ll in landline:
                        if ClientLandline.objects.filter(client=client,
                                                         landline=str(ll)).exists():
                            continue
                        else:
                            ClientLandline.objects.get_or_create(client=client,
                                                                 landline=str(ll))
                else:
                    landline_objs.delete()
                    if len(landline) > 0:
                        for ll in landline:
                            ClientLandline.objects.create(landline=str(ll),
                                                          client=client)

        client.save()
    except Exception as e:
        app.logger.debug(str(e))
        return "ErrorUpdatingClient"
    try:
        bid = client.billing_addressid
        baddress = BillingAddress.objects.get(id=bid)
        baddress.state = data.get('state')
        baddress.address_line1 = data.get('address_line1')
        baddress.city = data.get('city')
        baddress.pin_code = data.get('pin_code')
        baddress.area = data.get('area')
        baddress.save()

        sid = client.shipping_addressid
        saddress = ShippingAddress.objects.get(id=sid)
        saddress.state = data.get('state')
        saddress.address_line1 = data.get('address_line1')
        saddress.city = data.get('city')
        saddress.pin_code = data.get('pin_code')
        saddress.area = data.get('area')
        saddress.save()

    except Exception as e:
        app.logger.debug(str(e))
        return "ErrorUpdatingAddress"
    return {"client_id": client.client_id}

from uni_db.client_erp.models import (Client, ClientComment, BillingAddress,
                                      ShippingAddress, AddCall, CallTag,
                                      ClientMobile, ClientWhatsapp,
                                      ClientLandline)
# from DBLayer.order_management.models import Order, OrderItem
from clientservice.utils.utility_functions import (get_str_datetime)
from django.db.models import Q
from django.forms.models import model_to_dict
from datetime import datetime
from flask import current_app as app


def get_client_datails(data):
    try:
        client_id = data.get('client_id', '').strip('/')
        client = Client.objects.get(client_id=client_id)
    except Client.DoesNotExist:
        return "ClientNotFound"
    try:
        cdata = model_to_dict(client)
        cdata["billing_address"] = []
        cdata["shipping_address"] = []
        bill_ads = BillingAddress.objects.get(client=client)
        ship_ads = ShippingAddress.objects.get(client=client)
        ba = model_to_dict(bill_ads)
        sa = model_to_dict(ship_ads)
        cdata["billing_address"].append(ba)
        cdata["shipping_address"].append(sa)
        mobile_nos = ClientMobile.objects.filter(client=client)
        if mobile_nos:
            cdata["mobile"] = [str(mob.mobile) for mob in mobile_nos]
        else:
            cdata["mobile"] = "Not Available"
        whatsapp_nos = ClientWhatsapp.objects.filter(client=client)
        if whatsapp_nos:
            cdata["whatsapp"] = [str(wapp.whatsapp) for wapp in whatsapp_nos]
        else:
            cdata["whatsapp"] = "Not Available"
        landline_nos = ClientLandline.objects.filter(client=client)
        if landline_nos:
            cdata["landline"] = [str(ll.landline) for ll in landline_nos]
        else:
            cdata["landline"] = "Not Available"
#         for bill_ad in bill_ads:
#             ba = {
#                 "id": bill_ad.id,
#                 "state": bill_ad.state,
#                 "district": bill_ad.district,
#                 "taluka": bill_ad.taluka,
#                 "post_office": bill_ad.post_office,
#                 "pin_code": bill_ad.pin_code,
#                 "village": bill_ad.village,
#                 "other_taluka": bill_ad.other_taluka,
#                 "street": bill_ad.street,
#             }
#             fdata["billing_addresses"].append(ba)
#  
#         ship_ads = ShippingAddress.objects.filter(farmer=farmer)
#  
#         for ship_ad in ship_ads:
#             sa = {
#                 "id": ship_ad.id,
#                 "state": ship_ad.state,
#                 "district": ship_ad.district,
#                 "taluka": ship_ad.taluka,
#                 "post_office": ship_ad.post_office,
#                 "pin_code": ship_ad.pin_code,
#                 "village": ship_ad.village,
#                 "other_taluka": ship_ad.other_taluka,
#                 "street": ship_ad.street,
#             }
        cdata["last_modified"] = get_str_datetime(client.last_modified)
        cdata["created_on"] = get_str_datetime(client.created_on)
        try:
            cdata["created_by"] = client.entered_by.get_full_name()
        except:
            pass
 
        try:
            cdata["modified_by"] = client.modified_by.get_full_name()
        except:
            pass
 
#         fdata["orders"] = []
#         orders = Order.objects.filter(owner=farmer).order_by('-created_on')
#         for order in orders:
#             order_info = {
#                 "sales_order_id": order.sales_order_id,
#                 "created_on": get_str_datetime(order.created_on),
#                 "advance_payment": order.advance_payment,
#                 "total_discount": order.total_discount,
#                 "cod_amount": order.cod_amount,
#                 "grand_total": order.grand_total,
#                 "status": order.status,
#             }
#             try:
#                 if order.entered_by:
#                     order_info["entered_by"] = order.entered_by.get_full_name()
#             except:
#                 pass
#             fdata["orders"].append(order_info)
#  
#         valid_orders = orders.exclude(status__in=['CANCELLED', 'ERROR']).exclude(
#                 status__startswith="EDITED")
#         fdata["order_count"] = len(valid_orders)
#         if orders and orders[0].created_on:
#             last_order = orders[0]
#             today = datetime.today()
#             last_active = abs((today.date() - last_order.created_on.date())).days
#             if last_active == 0:
#                 fdata["last_active"] = "Today"
#             elif last_active < 31:
#                 fdata["last_active"] = str(last_active) + " Days"
#             else:
#                 fdata["last_active"] = str(int(round(last_active/30.0))) + " Month"
 
        comments = [
            {
                "comment": c.comment,
                "commented_by": c.commented_by.get_full_name(),
                "comment_time": get_str_datetime(c.comment_time)
            }
            for c in ClientComment.objects.filter(client=client)
        ]
        cdata["comments"] = comments
#         related_orders = Order.objects.filter(shipping_address__post_office=str(ship_ads[0].post_office)
#                                               ).exclude(status='RETURN COMPLETED'
#                                                         ).exclude(status='CANCELLED'
#                                                                   ).order_by('-sales_order_id')[:5]
#         farmer_data = {}
#          
#         if len(related_orders) < 5 and len(related_orders) >= 0:
#             farmer_data['order'] = [{
#                                      'order_id': str(ord.sales_order_id),
#                                      'name': str((ord.owner.first_name).title()) + \
#                                      " " + str((ord.owner.middle_name).title()) + \
#                                      " " + str((ord.owner.last_name).title()),
#                                      'status': str(ord.status),
#                                      'order_item': [str(item.item_name).split('-')[1]
#                                                     for item in
#                                                     OrderItem.objects.filter(order=ord)]
#                                      }for ord in related_orders]
#             farmer_data['farmer'] = [{
#                                       'farmer_id': str(sa.farmer.farmer_id),
#                                       'name': str((sa.farmer.first_name).title()) + \
#                                       " " + str((sa.farmer.middle_name).title()) + \
#                                       " " + str((sa.farmer.last_name).title())
#                                       }for sa in
#                                      ShippingAddress.objects.filter
#                                      (post_office=ship_ads[0].post_office
#                                       ).order_by('-id')[:5]]
#         else:
#             farmer_data['order'] = [{
#                                      'order_id': str(ord.sales_order_id),
#                                      'name': str((ord.owner.first_name).title()) + \
#                                      " " + str((ord.owner.middle_name).title()) + \
#                                      " " + str((ord.owner.last_name).title()),
#                                      'status': str(ord.status),
#                                      'order_item': [str(item.item_name).split('-')[1]
#                                                     for item in
#                                                     OrderItem.objects.filter(order=ord)]
#                                      }for ord in related_orders]
#         fdata['related_data'] = farmer_data
        call_list = []
        calls_data = AddCall.objects.filter(client=client)
        for calldata in calls_data:
            call_dict = {}
            tags = []
            call_dict['created_date'] = (calldata.created_date).strftime("%d/%m/%Y")
            call_dict['created_by'] = str(calldata.created_by.username)
            call_tags = CallTag.objects.filter(call=calldata)
            for tag in call_tags:
                tags.append(tag.tags)
            call_dict['tags'] = tags
            call_list.append(call_dict)
        cdata['call_history'] = call_list
        return cdata
 
    except Exception as e:
        app.logger.debug(str(e))
        return {
            'responseCode': 503,
            'Message': "Error in getting Client Details"
        }


def search_client_details(data):
    app.logger.info("Received Search Client Request")
    if not data.get('search_type') and not data.get('search_term'):
        return {
            'errorCode': 503,
            'errorMessage': "Parameters not found"
        }

    final_clients = []
    if data.get('search_type') == "mobile":
        clients = [cl_mob.client
                   for cl_mob in
                   ClientMobile.objects.filter(mobile=data.get('search_term'))]
        if not clients:
            other_matches = [cl_wt.client
                             for cl_wt in
                             ClientWhatsapp.objects.filter(whatsapp=data.get('search_term'))]
            for c in other_matches:
                if c not in clients:
                    clients.append(c)
        landline_clients = [cl_ll.client
                            for cl_ll in
                            ClientLandline.objects.filter(landline=data.get('search_term'))]
        final_clients = clients + landline_clients

    elif data.get('search_type') == "name":
        if data.get('search_term'):
            final_clients = list(Client.objects.filter(client_name__icontains=
                                                       data.get('search_term')))
    elif data.get('search_type') == "area":
        if data.get('search_term'):
            final_clients = [baddr.client
                             for baddr in
                             BillingAddress.objects.filter(area__icontains=data.get('search_term'))]
    clientdata = []
    for client in final_clients:
        c = {
            "client_id": client.client_id,
            "name": client.client_name,
            "mobile": [cl_mb.mobile for cl_mb in ClientMobile.objects.filter(client=client)],
            "whatsapp": [cl_wt.whatsapp for cl_wt in ClientWhatsapp.objects.filter(client=client)],
            "landline": [cl_ll.landline for cl_ll in ClientLandline.objects.filter(client=client)],
        }
        if client.billing_addressid:
            b = BillingAddress.objects.get(id=client.billing_addressid)
            c["address"] = model_to_dict(b)
            c["order_count"] = '2'
        clientdata.append(c)
    return clientdata
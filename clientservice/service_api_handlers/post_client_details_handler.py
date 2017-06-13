from uni_db.client_erp.models import (Client, ClientComment, BillingAddress,
                                      ShippingAddress, AddCall, CallTag,
                                      ClientMobile, ClientWhatsapp,
                                      ClientLandline)

from clientservice.utils.auth import get_user
from flask import current_app as app


def handle_request(data):
    print data
    return data
#     try:
#         c = Client(first_name=data.get('first_name'),
#                    middle_name=data.get('middle_name'),
#                    last_name=data.get('last_name'),
#                    referer=data.get('reference'),
#                    entered_by=get_user(),
#                    modified_by=get_user()
#                    )
#         contact = data['contactInformation']
#         numbers = contact['numbers']
#         if len(numbers) > 0:
#             f.mobile_1 = numbers[0]
#         if len(numbers) > 1:
#             f.mobile_2 = numbers[1]
#         if len(numbers) > 2:
#             f.mobile_3 = numbers[2]
#         if int(data.get('farmer_insurance')) == 1:
#             f.crop_insurance = True
#         if int(data.get('farmer_irrigation')) == 1:
#             f.drip_irrigation = True
#         if int(data.get('farmer_tractor')) == 1:
#             f.tractor = True
#         f.save()
#     except Exception as e:
#         app.logger.debug(str(e))
#         return {
#             "errorCode": "503",
#             "errorMessage": "Error creating farmer profile"
#         }
# 
#     try:
#         baddress = BillingAddress.objects.create(
#             farmer=f,
#             state=data.get('state'),
#             district=data.get('district'),
#             taluka=data.get('taluka'),
#             post_office=data.get('post_office'),
#             pin_code=data.get('pin_code'),
#             street=data.get('street_address', ''),
#             village=data.get('village', ''),
#             other_taluka=data.get('other_taluka', '')
#         )
# 
#         saddress = ShippingAddress.objects.create(
#             farmer=f,
#             state=data.get('state'),
#             district=data.get('district'),
#             taluka=data.get('taluka'),
#             post_office=data.get('post_office'),
#             pin_code=data.get('pin_code'),
#             street=data.get('street_address', ''),
#             village=data.get('village', ''),
#             other_taluka=data.get('other_taluka', '')
#         )
#         f.billing_addressid = baddress.id
#         f.shipping_addressid = saddress.id
#         f.save()
#     except Exception as e:
#         app.logger.debug(str(e))
#         return {
#             "errorCode": "503",
#             "errorMessage": "Error in saving farmer address"
#         }
#     if 'crop_information' in data:
#         crop_info = data['crop_information']
#         print crop_info
#         for itr in range(0, len(crop_info)):
#             crop_area = str(crop_info[itr]['farm_area'])
#             if crop_info[itr]['crop_type'] == "Future":
#                 crop_type = True
#             else:
#                 crop_type = False
#             if crop_area != '':
#                 farm_area = float(str(crop_info[itr]['farm_area']))
#                 CropInformation.objects.create(farmer=f,
#                                                crop=crop_info[itr]['crop'],
#                                                season=crop_info[itr]['season'],
#                                                area=farm_area,
#                                                unit=crop_info[itr]['area_unit'],
#                                                is_future=crop_type)
#             else:
#                 CropInformation.objects.create(farmer=f,
#                                                crop=crop_info[itr]['crop'],
#                                                season=crop_info[itr]['season'],
#                                                is_future=crop_type)
#     return {
#         "farmer_id": f.farmer_id
#     }
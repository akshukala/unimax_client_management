from flask import request
from django.core.exceptions import ObjectDoesNotExist
from flask import current_app as app
from flask.globals import request
from datetime import datetime, timedelta, time, tzinfo
from django.db.models import Q
import requests
import json
import urllib
from clientservice.utils.resource import Resource
from uni_db.client_erp.models import ScheduleCalls, Agent, ClientMobile
from clientservice.utils.auth import get_user


class ScheduleCall(Resource):

    def get(self):
        try:
            today = datetime.now().date()
            tomorrow = today + timedelta(1)
            today_end = datetime.combine(tomorrow, time())
            response = []
            for call in ScheduleCalls.objects.filter(associated_to=Agent.objects.get(user=get_user()),
                                                     schedule_date__lt=today_end,
                                                     replied_back=False)[::-1]:
                call_dict = {}
                call_dict['call_id'] = str(call.id)
                call_dict['mobile_no'] = str(call.phone)
                call_dict['note'] = str(call.note)
                scheduleDate = call.schedule_date
                tz_info = scheduleDate.tzinfo
                difference = datetime.now(tz_info) - scheduleDate
                if difference.days != 0 and difference.days != -1:
                    call_dict['time_difference'] = str(difference.days) +" day and  "+ call.schedule_date.strftime('%H:%M') + " hours ago."
                    call_dict['time_parameter'] = 1
                else:
                    call_dict['time_difference'] = "Today " + call.schedule_date.strftime('%H:%M') + "."
                    call_dict['time_parameter'] = 0
                mobile = call.phone[3:]
                try:
                    client_obj = ClientMobile.objects.filter(mobile=str(mobile))[0]
                    call_dict['client_id'] = str(client_obj.client.client_id)
                    call_dict['client_name'] = str((client_obj.client.client_name).title())
                except ObjectDoesNotExist:
                    call_dict['client_name'] = "Client Name not available."
                    call_dict['client_id'] = "No id available"
                response.append(call_dict)
            if len(response) > 0:
                return {"responseCode": 200,
                        "response": response}
            else:
                return {"responseCode": 201,
                        "Message": "No Scheduled Calls for today"}
        except:
            return {"responseCode": 400,
                    "Message": """Something went wrong"""}

    def post(self):
        request_data = request.get_json(force=True)
        try:
            schedule_date = datetime.strptime(str(request_data.get('schedule_date')), '%Y-%m-%d %H:%M:%S')
            ScheduleCalls.objects.create(phone=str(request_data.get('mobile_no')),
                                         replied_back=False, schedule_date=schedule_date,
                                         associated_to=Agent.objects.get(user=get_user()),
                                         note=str(request_data.get('note')))
            return {"responseCode": 200,
                    "Message": """Call Scheduled Successfully"""}
        except:
            return {"responseCode": 400,
                    "Message": """Something went wrong"""}

    def put(self):
        request_data = request.get_json(force=True)
        try:
            ScheduleCalls.objects.filter(id=int(request_data.get('call_id'))).update(replied_back=True)
            return {"responseCode": "200",
                    "Message": """Call Successfully marked as call made"""}
        except:
            return {"responseCode": "400",
                    "Message": """Something went wrong"""}
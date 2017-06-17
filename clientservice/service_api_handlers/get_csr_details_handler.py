from uni_db.client_erp.models import Client
from uni_db.order_management.models import Order, OrderItem
from clientservice.utils.utility_functions import (
    get_str_date, get_str_datetime
)

from flask import current_app as app
from clientservice.utils.auth import get_user
from datetime import datetime, timedelta


def handle_request():
    try:
        Customer = get_user()
        today = datetime.today().date()
        orders_today = Order.objects.filter(
            entered_by=Customer, created_on__startswith=today
            ).order_by('-created_on')

        orders_count = orders_today.exclude(status="CANCELLED").count()

        orders = []
        for o in orders_today:
            order_items = OrderItem.objects.filter(order=o)
            orderItemList = []
            orderQuantityList = []
            for oi in order_items:
                itemname = oi.item_name.split('-')
                orderItemList.append(itemname[1])
                orderQuantityList.append(oi.quantity)
            orders.append({
                "sales_order_id": o.sales_order_id,
                "client": o.owner.client_id,
                "client_name": o.owner.client_name,
                "grand_total": o.cod_amount,
                "created_on": get_str_datetime(o.created_on),
                "status": o.status,
                "address_line1": o.billing_address.address_line1,
                "area": o.billing_address.area,
                "city": o.billing_address.city,
                "state": o.billing_address.state,
                "pin": o.billing_address.pin_code,
                "orderitems": orderItemList,
                "quantity": orderQuantityList
            })

        yesterday = today - timedelta(days=1)
        orders_yesterday = Order.objects.filter(
            entered_by=Customer, created_on__startswith=yesterday).exclude(
                status="CANCELLED").count()

        this_month = today.strftime('%Y-%m')
        order_this_month = Order.objects.filter(
            entered_by=Customer, created_on__startswith=this_month).exclude(
                status="CANCELLED").count()

        last_month = (today.replace(day=1) - timedelta(days=1)).strftime("%Y-%m")
        order_last_month = Order.objects.filter(
            entered_by=Customer, created_on__startswith=last_month).exclude(
                status="CANCELLED").count()

        past_week = (datetime.today() - timedelta(days=7)).date()
        advance_orders = Order.objects.filter(
            advance_order_date__gt=past_week,
            entered_by=Customer,
            status="FUTURE ORDER").exclude(
                advance_order_date__gt=today).order_by('-advance_order_date')

        adv_orders_json = [{
            "sales_order_id": o.sales_order_id,
            "status": o.status,
            "advance_order_date": get_str_date(o.advance_order_date)
            } for o in advance_orders]

        clients = Client.objects.filter(
            entered_by=Customer, created_on__startswith=today
            ).count()

        response = {
            "Customer": Customer.get_full_name(),
            "orders_today": orders,
            "orders_count": orders_count,
            "advance_orders": adv_orders_json,
            "new_clients": clients,
            "orders_yesterday": orders_yesterday,
            "orders_this_month": order_this_month,
            "orders_last_month": order_last_month,
            "last_login": (Customer.last_login).strftime("%a, %d. %b %Y %I:%M%p")
        }

        return {
            "responseCode": 200,
            "info": response
        }

    except Exception as e:
        app.logger.debug(str(e))
        return {
            'responseCode': 503,
            'Message': "Error in getting Executive Details"
        }


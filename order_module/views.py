from django.shortcuts import redirect,render
from django.http import HttpRequest,HttpResponse,JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from product_module.models import Product
from .models import Order,OrderDetail
import requests
import json
import time


# Zarinpal (SANDBOX)
ZP_MERCHANT_ID = "00000000-0000-0000-0000-000000000000"  # هر UUID دلخواه
ZP_REQUEST_URL = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
ZP_VERIFY_URL  = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
ZP_STARTPAY    = "https://sandbox.zarinpal.com/pg/StartPay/{authority}"
ZP_CALLBACK_URL = "http://127.0.0.1:8000/order/verify-payment"  # آدرس برگشت
amount = 11000  # Rial / Required
description = "نهایی کردن خرید شما از سایت ما"  # Required
email = ''  # Optional
mobile = ''  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/order/verify-payment'


def addProductToOrder(request:HttpRequest):
    product_id=int(request.GET.get('product_id'))
    product_count=int(request.GET.get('product_count'))
    if product_count < 1:
        return JsonResponse({
                'status':'invalid_count',
                'icon':'warning',
                'text':'مقدار وارد شده غیرمعتبر است',
                'confirm_button_text':'متوجه شدم'
            })

    if request.user.is_authenticated:
        product=Product.objects.filter(id=product_id,is_active=True,is_delete=False).first()
        if product is not None:
            current_order,created=Order.objects.get_or_create(is_paid=False,user_id=request.user.id)
            current_detail=current_order.orderdetail_set.filter(product_id=product_id).first()
            if current_detail is not None:
                current_detail.count += product_count
                current_detail.save()
            else:
                new_detail=OrderDetail(order_id=current_order.id,product_id=product_id,count=product_count)
                new_detail.save()

            return JsonResponse({
                'status':'success',
                'icon':'success',
                'text':'محصول با موفقیت به سبد خرید اضافه شد',
                'confirm_button_text':'مشاهده سبد خرید'
            })
    else:
        return JsonResponse({
            'status':'not_auth',
            'icon':'error',
            'text':'برای خرید و سفارش ابتدا می بایست لاگین شوید',
            'confirm_button_text':'انتقال به صفحه لاگین'
            })
    
@login_required
def request_payment(request:HttpRequest):
    current_order,created=Order.objects.get_or_create(is_paid=False,user_id=request.user.id)
    total_price=current_order.get_total_amount()
    if total_price == 0:
        return redirect(reverse('user_basket_page'))
    
    req_data = {
        "merchant_id": ZP_MERCHANT_ID,
        "amount": total_price * 10,
        "callback_url": CallbackURL,
        "description": description,
        # "metadata": {"mobile": mobile, "email": email}
    }
    req_header = {"accept": "application/json", "content-type": "application/json'"}
    req = requests.post(url=ZP_REQUEST_URL, data=json.dumps(req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_STARTPAY .format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")

@login_required
def verify_payment(request:HttpRequest):
    current_order,created=Order.objects.get_or_create(is_paid=False,user_id=request.user.id)
    total_price=current_order.get_total_amount()
    t_authority = request.GET['Authority']
    if total_price == 0:
        return redirect(reverse('user_basket_page'))
    
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json", "content-type": "application/json'"}
        req_data = {
            "merchant_id": ZP_MERCHANT_ID,
            "amount":total_price *10,
            "authority": t_authority
        }
        req = requests.post(url=ZP_VERIFY_URL, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                # return HttpResponse('Transaction success.\nRefID: ' + str(
                #     req.json()['data']['ref_id']
                # ))
                current_order.is_paid=True
                current_order.paymentDate=time.time()
                current_order.save()
                str_ref=req.json()['data']['ref_id']
                return render(request,'order_module/payment_response.html',{
                    'success':f'تراکنش با کد پیگیری{str_ref} با موفقیت انجام شد'
                })
            elif t_status == 101:
                # return HttpResponse('Transaction submitted : ' + str(
                #     req.json()['data']['message']
                # ))
                return render(request,'order_module/payment_response.html',{
                    'info':'این تراکنش قبلا انجام شده است'
                })
            else:
                # return HttpResponse('Transaction failed.\nStatus: ' + str(
                #     req.json()['data']['message']
                # ))
                return render(request,'order_module/payment_response.html',{
                    'error':str(req.json()['data']['message'])
                })
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return render(request,'order_module/payment_response.html',{
                 'error':f"Error code: {e_code}, Error Message: {e_message}"
            })
    else:
        return render(request,'order_module/payment_response.html',{
            'error':'پرداخت با خطا مواجه شد/کاربر از پرداخت ممانعت کرد'
         })
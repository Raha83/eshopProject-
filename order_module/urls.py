from django.urls import path
from . import views

urlpatterns=[
    path('add-to-cart',views.addProductToOrder,name='addToCart'),
    path('request-payment', views.request_payment, name='request_payment'),
    path('verify-payment', views.verify_payment , name='verify_payment')
]

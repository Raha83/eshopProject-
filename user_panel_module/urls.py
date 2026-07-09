from django.urls import path
from . import views

urlpatterns=[
    path('',views.UserPanelDashboardPage.as_view(),name='user_panel_page'),
    path('edit-profile',views.EditProfilePage.as_view(),name='edit_profile_page'),
    path('change-password',views.ChangePasswordPage.as_view(),name='change_pass_page'),
    path('user-basket',views.user_basket,name='user_basket_page'),
    path('my-shopping',views.MyShopping.as_view(),name='show_order_page'),
    path('my-shopping-detail/<order_id>',views.my_shopping_detail,name='show_order_detail_page'),
    path('user-order-remove',views.remove_order_detail,name='remove_order_page'),
    path('user-order-quantity',views.change_order_quantity,name='order_quantity_page')
]
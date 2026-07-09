from django.urls import path
from . import views

urlpatterns=[
    path('register/',views.RegisterView.as_view(),name='register_page'),
    path('login/',views.LoginView.as_view(),name='login_page'),
    path('logout/',views.LogOutView.as_view(),name='logout_page'),
    path('forget-pass/',views.ForgetPasswordView.as_view(),name='forget_pass_page'),
    path('reset-pass/<active_code>',views.ResetPasswordView.as_view(),name='reset_pass_page'),
    path('active-code/<email_active_code>',views.ActivateView.as_view(),
    name='active_code_page')
]
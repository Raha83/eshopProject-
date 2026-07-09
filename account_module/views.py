from django.shortcuts import render,redirect,reverse
from django.http import Http404,HttpRequest
from django.views.generic import View
from .forms import RegisterForm,LoginForm,ForgetPassForm,ResetPassForm
from .models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import login,logout
from utils.email_service import send_email

# Create your views here.

class RegisterView(View):
    def get(self,request):
        register_form=RegisterForm()
        context={
            'register_form':register_form
        }
        return render(request,'account_module/register.html',context)
    def post(self,request):
        register_form=RegisterForm(request.POST)
        if register_form.is_valid():
            user_email=register_form.cleaned_data.get('email')
            user_password=register_form.cleaned_data.get('password')
            user:bool=User.objects.filter(email__iexact=user_email).exists()

            if user:
                register_form.add_error('email','کاربر با این ایمیل قبلا ثبت نام شده')
            else:
                new_user=User(email=user_email,email_active_code=get_random_string(48),
                is_active=False,username=user_email)
                new_user.set_password(user_password)
                new_user.save()
                send_email('فعالسازی حساب کاربری',new_user.email,{'user':new_user},
                'emails/active_account.html')
                return redirect(reverse('login_page'))
            
        context={
            'register_form':register_form
        }
        return render(request,'account_module/register.html',context)


class LoginView(View):
    def get(self,request):
        login_form=LoginForm()
        context={
            'login_form':login_form
        }
        return render(request,'account_module/login.html',context)
    def post(self,request:HttpRequest):
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            user_email=login_form.cleaned_data.get('email')
            user_password=login_form.cleaned_data.get('password')
            user:User=User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                 if not user.is_active:
                    login_form.add_error('email','حساب کاربری شما هنوز فعال نشده')

                 confirm_password=user.check_password(user_password)
                 if confirm_password:
                    login(request,user)
                    return redirect(reverse('home_page'))
                 else:
                    login_form.add_error('email','کاربری با این مشخصات یافت نشد')
            else:
                login_form.add_error('email','کاربری با این مشخصات یافت نشد')
        context={
            'login_form':login_form
        }
        return render(request,'account_module/login.html',context)


class ActivateView(View):
    def get(self,request,email_active_code):
        user : User= User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active=True
                user.email_active_code=get_random_string(48)
                user.save()
                # todo : show success message to user
                return redirect(reverse('login_page'))
            else:
                # todo: show you are active message to user
                pass

        raise Http404
       

class ForgetPasswordView(View):
    def get(self,request:HttpRequest):
        forget_pass_form=ForgetPassForm()
        context={
            'forget_pass_form':forget_pass_form
        }
        return render(request,'account_module/forget_pass.html',context)
    def post(self,request:HttpRequest):
        forget_pass_form=ForgetPassForm(request.POST)
        if forget_pass_form.is_valid():
            user_email=forget_pass_form.cleaned_data.get('email')
            user : User=User.objects.filter(email__iexact=user_email).first()
            if user is None:
                forget_pass_form.add_error('email','کاربر با این مشخصات یافت نشد')
            else:
                send_email('بازیابی کلمه عبور',user.email,{'user':user},
                'emails/reset_password.html')

        context={
            'forget_pass_form':forget_pass_form
        }
        return render(request,'account_module/forget_pass.html',context)
            

class ResetPasswordView(View):
    def get(self,request:HttpRequest,active_code):
        reset_pass_form=ResetPassForm()
        user: User=User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect(reverse('login_page'))
        context={
            'reset_pass_form':reset_pass_form,
            'user':user
        }
        return render(request,'account_module/reset_pass.html',context)

    def post(self,request:HttpRequest,active_code):
        reset_pass_form=ResetPassForm(request.POST)
        if reset_pass_form.is_valid():
             user : User=User.objects.filter(email_active_code__iexact=active_code).first()
             user_password=reset_pass_form.cleaned_data.get('password')
             if user is None:
                return redirect(reverse('login_page'))
             user.set_password(user_password)
             user.email_active_code=get_random_string(48)
             user.is_active=True
             user.save()
             return redirect(reverse('login_page'))

        context={
            'user':user,
            'reset_pass_form':reset_pass_form
        }
        return render(request,'account_module/reset_pass.html',context)


class LogOutView(View):
    def get(self,request):
        logout(request)
        return redirect(reverse('login_page'))



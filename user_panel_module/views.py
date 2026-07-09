from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import TemplateView, View,ListView
from django.http import HttpRequest,Http404,JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import EditProfileModelForm, ChangePassForm
from account_module.models import User
from order_module.models import Order,OrderDetail

# Create your views here.

@method_decorator(login_required,'dispatch')
class UserPanelDashboardPage(TemplateView):
    template_name = 'user_panel_module/user_panel_dashboard_page.html'

@method_decorator(login_required,'dispatch')
class EditProfilePage(View):
    def get(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        form = EditProfileModelForm(instance=current_user)
        context = {
            'form': form,
            'current_user': current_user
        }
        return render(request, 'user_panel_module/edit_profile_page.html', context)

    def post(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        form = EditProfileModelForm(
            request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save()
        context = {
            'form': form,
            'current_user': current_user
        }
        return render(request, 'user_panel_module/edit_profile_page.html', context)

@method_decorator(login_required,'dispatch')
class ChangePasswordPage(View):
    def get(self, request: HttpRequest):
        change_pass_form = ChangePassForm()
        context = {
            'change_pass_form': change_pass_form
        }
        return render(request, 'user_panel_module/change_pass_page.html', context)

    def post(self, request: HttpRequest):
        change_pass_form = ChangePassForm(request.POST)
        if change_pass_form.is_valid():
            current_user: User = User.objects.filter(
                id=request.user.id).first()
            if current_user.check_password(change_pass_form.cleaned_data.get('current_password')):
                current_user.set_password(
                    change_pass_form.cleaned_data.get('new_password'))
                current_user.save()
                logout(request)
                return redirect(reverse('login_page'))
            else:
                change_pass_form.add_error('current_password','کلمه عبور وارد شده صحیح نیست')

        context = {
            'change_pass_form': change_pass_form
        }
        return render(request, 'user_panel_module/change_pass_page.html', context)

@method_decorator(login_required,'dispatch')
class MyShopping(ListView):
    model=Order
    template_name='user_panel_module/order_list_page.html'

    def get_queryset(self):
        query=super().get_queryset()
        request:HttpRequest=self.request
        query=query.filter(user_id=request.user.id,is_paid=True)
        return query

@login_required
def user_panel_menu_component(request: HttpRequest):
    return render(request, 'user_panel_module/components/user_dashboard_menu_component.html')

@login_required
def user_basket(request : HttpRequest):
    current_order,created=Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,user_id=request.user.id)
    total_amount=current_order.get_total_amount()
    context={
        'current_order':current_order,
        'total_amount':total_amount
    }
    return render(request,'user_panel_module/user_basket.html',context)

@login_required
def remove_order_detail(request):
    detail_id=request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({
            'status':'not_found_detail_id'
        })
    
    delete_count,delete_dic=OrderDetail.objects.filter(id=detail_id,order__is_paid=False,order__user_id=request.user.id).delete()
    if delete_count == 0:
        return JsonResponse({
            'status':'not_found_detail'
        })
    
    current_order,created=Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,user_id=request.user.id)
    total_amount=current_order.get_total_amount()
    context={
        'current_order':current_order,
        'total_amount':total_amount
    }
    return JsonResponse({
        'status':'success',
        'body':render_to_string('user_panel_module/user_basket_content.html',context)
    })

@login_required
def change_order_quantity(request):
    detail_id=request.GET.get('detail_id')
    state=request.GET.get('state')
    
    if detail_id is None or state is None:
        return JsonResponse({
            'status':'not_found_detail_id_state'
        })
    
    current_detail=OrderDetail.objects.filter(id=detail_id,order__is_paid=False,order__user_id=request.user.id).first()
    if current_detail is None:
        return JsonResponse({
            'status': 'detail_not_found'
        })
    
    if state == 'increase':
        current_detail.count +=1
        current_detail.save()
    elif state == 'decrease':
        if current_detail.count == 1:
            current_detail.delete()
        else:
            current_detail.count -=1
            current_detail.save()
    else:
        return JsonResponse({
            'status':'invalid_state'
        })

    current_order,created=Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,user_id=request.user.id)
    total_amount=current_order.get_total_amount()
    context={
        'current_order':current_order,
        'total_amount':total_amount
    }
    return JsonResponse({
        'status':'success',
        'body':render_to_string('user_panel_module/user_basket_content.html',context)
    })

@login_required
def my_shopping_detail(request:HttpRequest,order_id):
    order=Order.objects.prefetch_related('orderdetail_set').filter(id=order_id,user_id=request.user.id).first()
    if order is None:
        raise Http404('سبد خرید مورد نظر یافت نشد')
    context={
        'order':order
    }
    return render(request,'user_panel_module/user_order_detail.html',context)   
    

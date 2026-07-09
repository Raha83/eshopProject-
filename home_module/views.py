from django.shortcuts import render
from django.db.models import Count,Sum
from django.views.generic.base import TemplateView
from site_module.models import SiteSetting, FooterLinkBox, Slider
from product_module.models import Product,ProductCategory
from utils.convertors import group_list

# Create your views here.


class HomeView(TemplateView):
    template_name = 'home_module/index_page.html'

    def get_context_data(self, **kwargs):
        # return super().get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)

        sliders = Slider.objects.filter(is_active=True)
        context['sliders'] = sliders
        latest_products = Product.objects.filter(
            is_active=True, is_delete=False).order_by('-id')[:12]
        visited_products = Product.objects.filter(is_active=True, is_delete=False).annotate(
            visit_count=Count('productvisit')).order_by('-visit_count')[:12]
        context['latest_products'] = group_list(latest_products)
        context['visited_products'] = group_list(visited_products)
        categories=list(ProductCategory.objects.annotate(product_count=Count('products')).filter(is_active=True,is_delete=False,product_count__gt=0)[:6])
        product_categories=[]
        for category in categories:
            item={
                'id':category.id,
                'title':category.title,
                'products':list(category.products.all()[:4])
            }
            product_categories.append(item)
        context['product_categories']=product_categories
        most_saled_products=Product.objects.filter(orderdetail__order__is_paid=True).annotate(order_count=Sum(
            'orderdetail__count'
        )).order_by('-order_count')[:12]
        context['most_saled_products']=group_list(most_saled_products)
        return context


class AboutView(TemplateView):
    template_name = 'home_module/about_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        site_setting: SiteSetting = SiteSetting.objects.filter(
            is_main_setting=True).first()
        context['site_setting'] = site_setting
        return context


def index_page(request):
    return render(request, 'home_module/index_page.html')

# class HomeView(View):
#     def get(self,request):
#         context={
#             'data':'this is my data'
#         }
#         return render(request,'home_module/index_page.html',context)


def site_header_component(request):
    site_setting: SiteSetting = SiteSetting.objects.filter(
        is_main_setting=True).first()

    context = {
        'site_setting': site_setting
    }
    return render(request, 'shared/site_header_component.html', context)


def site_footer_component(request):
    site_setting: SiteSetting = SiteSetting.objects.filter(
        is_main_setting=True).first()
    footer_links = FooterLinkBox.objects.all()
    for item in footer_links:
        item.footerlink_set

    context = {
        'site_setting': site_setting,
        'footer_links': footer_links
    }
    return render(request, 'shared/site_footer_component.html', context)

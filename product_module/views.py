from django.shortcuts import render
from django.http import HttpRequest
from django.db.models import Count
from .models import Product, ProductCategory, ProductBrand,ProductVisit,ProductGallery
from site_module.models import SiteBanner
from django.views.generic import ListView, DetailView
from utils.http_service import get_client_ip
from utils.convertors import group_list


class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by =6

    def get_queryset(self):
        query = super().get_queryset()
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')
        request: HttpRequest = self.request
        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')
        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)
        if brand_name is not None:
            query = query.filter(brand__url_title__iexact=brand_name)
        if start_price is not None:
            query = query.filter(price__gte=start_price)
        if end_price is not None:
            query = query.filter(price__lte=end_price)
        return query

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        query=Product.objects.all()
        product=query.order_by('-price').first()
        max_price=product.price if product is not None else 1000000
        request: HttpRequest = self.request
        start_price = request.GET.get('start_price') or 0
        end_price = request.GET.get('end_price') or max_price
        context['max_price']=max_price
        context['start_price']=start_price
        context['end_price']=end_price
        context['banners']=SiteBanner.objects.filter(is_active=True , position__iexact=SiteBanner.BannerChoices.product_list)
        return context


class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uploaded_object = self.object
        request = self.request
        object_id = request.session.get('productId')
        context['product_session'] = object_id == str(uploaded_object.id)
        context['banners']=SiteBanner.objects.filter(is_active=True , position__iexact=SiteBanner.BannerChoices.product_detail)
        gallery_list=list(ProductGallery.objects.filter(product_id=uploaded_object.id).all())
        gallery_list.insert(0,uploaded_object)
        context['product_galleries_group'] = group_list(gallery_list, 3)
        context['related_products']=group_list(list(Product.objects.filter(brand_id=uploaded_object.brand_id).exclude(pk=uploaded_object.id).all()[:12]),3)
        
        user_ip=get_client_ip(self.request)
        user_id=None
        if self.request.user.is_authenticated:
            user_id=self.request.user.id
        user=ProductVisit.objects.filter(ip__iexact=user_ip, product_id=uploaded_object.id).exists()
        if not user:
            new_user=ProductVisit(product=uploaded_object,user_id=user_id,ip=user_ip)
            new_user.save()
        return context


def product_categories_component(request: HttpRequest):
    product_category = ProductCategory.objects.filter(
        is_active=True, is_delete=False)
    context = {
        'categories': product_category
    }
    return render(request, 'product_module/components/product_categories_component.html', context)


def product_brands_component(request: HttpRequest):
    product_brand = ProductBrand.objects.annotate(
        product_count=Count('product')).filter(is_active=True)
    context = {
        'brands': product_brand
    }
    return render(request, 'product_module/components/product_brands_component.html', context)

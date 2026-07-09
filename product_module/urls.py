from django.urls import path
from . import views
urlpatterns=[
    path('',views.ProductListView.as_view(),name='product-list'),
    path('cat/<cat>',views.ProductListView.as_view(),name='product-list-by-category'),
    path('brand/<brand>',views.ProductListView.as_view(),name='product-list-by-brand'),
    path('<int:pk>',views.ProductDetailView.as_view(),name='product-detail')
]
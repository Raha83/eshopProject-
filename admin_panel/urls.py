from django.urls import path
from . import views

urlpatterns=[
    path('',views.dashboard,name='admin_dashboard'),
    path('articles/',views.ArticleListView.as_view(),name='articles_list'),
    path('articles/edit/<pk>',views.ArticleEditView.as_view(),name='articles_edit')
]
from django.urls import path
from . import views

urlpatterns=[
    path('',views.ArticleListView.as_view(),name='article_page'),
    path('cat/<str:category>',views.ArticleListView.as_view(),name='article_by_category'),
    path('<pk>/',views.ArticleDetailView.as_view(),name='article_detail_page'),
     # /due to next path to be capable of reading and not replacing
    path('article-add-comment',views.article_add_comment,name='article_add_comment')
] 
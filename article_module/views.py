from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.http import HttpRequest, HttpResponse
from .models import Article, ArticleCategory, ArticleViewpoint
from jalali_date import datetime2jalali, date2jalali

# Create your views here.

class ArticleListView(ListView):
    template_name = 'article_module/articles_page.html'
    model = Article
    paginate_by = 4

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # context['date']=date2jalali(self.request.user.date_joined)
        return context

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(is_active=True)
        category_name = self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(
                selected_categories__url_title__iexact=category_name)
        return query


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_module/article_detail_page.html'

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(is_active=True)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article: Article = kwargs.get('object')
        context['comments'] = ArticleViewpoint.objects.filter(
            selected_article_id=article.id, parent=None).order_by('-create_date').prefetch_related('articleviewpoint_set')
        context['comments_count'] = ArticleViewpoint.objects.filter(
            selected_article_id=article.id).count()
        return context


def article_categories(request: HttpRequest):
    article_main_category = ArticleCategory.objects.prefetch_related('articlecategory_set').filter(
        is_active=True, parent=None)
    context = {
        'main_category': article_main_category
    }
    return render(request, 'article_module/components/article_categories_component.html', context)


def article_add_comment(request: HttpRequest):
    if request.user.is_authenticated:
        article_id = request.GET.get('article_id')
        article_comment = request.GET.get('article_comment')
        article_parent = request.GET.get('parent_id')
        new_comment = ArticleViewpoint(
            selected_article_id=article_id, parent_id=article_parent, user=request.user, text=article_comment)
        new_comment.save()
        context = {
            'comments': ArticleViewpoint.objects.filter(selected_article_id=article_id, parent=None).order_by('-create_date').prefetch_related('articleviewpoint_set'),
            'comments_count': ArticleViewpoint.objects.filter(selected_article_id=article_id).count()
        }
        return render(request, 'article_module/includes/article_comments_partial.html', context)

    return HttpResponse('response')

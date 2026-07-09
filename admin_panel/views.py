from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView,UpdateView
from article_module.models import Article
from utils.my_decorators import permission_checker_decorator_factory

# Create your views here.

@permission_checker_decorator_factory({'permission_name':'admin_dashboard'})
def dashboard(request):
    return render(request,'admin_panel/home/index.html')


@method_decorator(permission_checker_decorator_factory({'permission_name':'article_list'}),name='dispatch')
class ArticleListView(ListView):
    template_name = 'admin_panel/articles/articles_list.html'
    model = Article
    paginate_by = 12

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(is_active=True)
        category_name = self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(
                selected_categories__url_title__iexact=category_name)
        return query


@method_decorator(permission_checker_decorator_factory(),name='dispatch')
class ArticleEditView(UpdateView):
    model=Article
    template_name='admin_panel/articles/article_edit.html'
    fields='__all__'
    success_url=reverse_lazy('articles_list')
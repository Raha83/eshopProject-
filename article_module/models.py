from django.db import models
from account_module.models import User
from jalali_date import date2jalali

# Create your models here.


class ArticleCategory(models.Model):
    parent = models.ForeignKey('ArticleCategory', on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name='والد دسته بندی')
    title = models.CharField(max_length=200, verbose_name='عنوان دسته بندی')
    url_title = models.CharField(
        max_length=200, unique=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')

    class Meta:
        verbose_name = 'دسته بندی مقاله'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.title


class Article(models.Model):
    selected_categories = models.ManyToManyField(ArticleCategory,
                                                 verbose_name='دسته بندی مقاله')
    title = models.CharField(max_length=300, verbose_name='عنوان مقاله')
    slug = models.SlugField(max_length=400, db_index=True, allow_unicode=True,
                            verbose_name=' عنوان در url')
    short_description = models.TextField(verbose_name='توضیحات کوتاه')
    text = models.TextField(verbose_name='متن مقاله')
    image = models.ImageField(
        upload_to='images/articles', verbose_name='تصویر مقاله')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, verbose_name='نویسنده', editable=False)
    create_date = models.DateTimeField(auto_now_add=True, editable=False,
                                       verbose_name='ثبت تاریخ')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def get_jalali_create_date(self):
        return date2jalali(self.create_date)

    def get_jalali_create_time(self):
        return self.create_date.strftime('%H:%M')

    def __str__(self):
        return self.title


class ArticleViewpoint(models.Model):
    selected_article = models.ForeignKey(
        Article, on_delete=models.CASCADE, verbose_name='انتخاب مقاله')
    parent = models.ForeignKey(
        'ArticleViewpoint', on_delete=models.CASCADE, null=True, blank=True, verbose_name='والد')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='کاربر')
    text = models.TextField(max_length=500, verbose_name='متن پیام')
    create_date = models.DateTimeField(auto_now_add=True, editable=False,
                                       verbose_name='تاریخ ثبت')

    class Meta:
        verbose_name = 'نظر مقاله'
        verbose_name_plural = 'نظرات'

    def get_jalali_create_date(self):
        return date2jalali(self.create_date)

    def get_jalali_create_time(self):
        return self.create_date.strftime('%H:%M')

    def __str__(self):
        return str(self.user)

from django.db import models

# Create your models here.

class SiteSetting(models.Model):
    site_name=models.CharField(max_length=200,verbose_name='عنوان سایت')
    site_url=models.CharField(max_length=200,verbose_name='دامنه سایت')
    address=models.CharField(max_length=200,verbose_name='ادرس')
    phone=models.CharField(null=True,blank=True,max_length=200,verbose_name='شماره تماس',)
    fax=models.CharField(null=True,blank=True,max_length=200,verbose_name='فکس')
    email=models.EmailField(null=True,blank=True,verbose_name='ادرس ایمیل')
    copy_right=models.TextField(verbose_name='متن کپی رایت')
    about_us_text=models.TextField(verbose_name='متن درباره ی ما')
    site_logo=models.ImageField(upload_to='images/site_setting',verbose_name='لوگو سایت')
    is_main_setting=models.BooleanField(verbose_name='تنظیمات اصلی')

    class Meta:
        verbose_name='تنظیمات سایت'
        verbose_name_plural='تنظیمات ' 

    def __str__(self):
        return self.site_name

class FooterLinkBox(models.Model):
    title=models.CharField(max_length=200,verbose_name='عنوان دسته بندی')

    class Meta:
        verbose_name='دسته بندی لینک های فوتر'
        verbose_name_plural='دسته بندی ها'
    
    def __str__(self):
        return self.title

class FooterLink(models.Model):
    title=models.CharField(max_length=200,verbose_name='عنوان لینک')
    url=models.URLField(verbose_name='ادرس لینک')
    footerlink_category=models.ForeignKey(FooterLinkBox,on_delete=models.CASCADE,
    verbose_name='دسته بندی')

    class Meta:
        verbose_name=' لینک فوتر'
        verbose_name_plural='لینک های فوتر'
    
    def __str__(self):
        return self.title

class Slider(models.Model):
    title=models.CharField(max_length=200,verbose_name='عنوان')
    url=models.URLField(max_length=500,verbose_name='لینک')
    url_title=models.CharField(max_length=200,verbose_name='عنوان لینک')
    description=models.TextField(max_length=200,verbose_name='توضیحات')
    image=models.ImageField(upload_to='images/sliders',verbose_name='تصویر اسایدر')
    is_active=models.BooleanField(default=True,verbose_name='فعال/غیرفعال')
    
    class Meta:
        verbose_name='اسلایدر'
        verbose_name_plural='اسلایدرها'

    def __str__(self):
        return self.title

# position_choices=[
#     ('product_list','لیست محصولات'),
#     ('product_detail','جزییات محصولات'),
#     ('article_page','صفحه مقالات')
# ]
class SiteBanner(models.Model):
    class BannerChoices(models.TextChoices):
        product_list='product_list','صفحه لیست محصولات',
        product_detail='product_detail','صفحه جزییات محصولات',
        article_list='article_list','صفحه لیست مقالات'
   
    title=models.CharField(max_length=200,verbose_name='عنوان بنر')
    url=models.URLField(max_length=400,null=True,blank=True,verbose_name='آدرس بنر')
    image=models.ImageField(upload_to='images/banners',verbose_name='تصویر')
    is_active=models.BooleanField(verbose_name='فعال/غیرفعال')
    position=models.CharField(max_length=200,choices=BannerChoices.choices,verbose_name='مکان بنر')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name='بنر'
        verbose_name_plural='بنرها'

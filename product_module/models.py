from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from account_module.models import User

# Create your models here.
class ProductCategory(models.Model):
    title=models.CharField(max_length=300,verbose_name="عنوان")
    url_title=models.CharField(max_length=300,verbose_name="عنوان در url")
    is_active=models.BooleanField(verbose_name="فعال/غیرفعال")
    is_delete=models.BooleanField(verbose_name="حذف")
    
    def __str__(self):
        return f"({self.title}-{self.url_title})"
    
    class Meta:
        verbose_name="دسته بندی"
        verbose_name_plural="دسته بندی ها"

class ProductBrand(models.Model):
    title=models.CharField(max_length=300,db_index=True,verbose_name="عنوان")
    url_title=models.CharField(max_length=300,null=True,blank=True,db_index=True,verbose_name="عنوان در url")
    is_active=models.BooleanField(verbose_name="فعال/غیرفعال")

    class Meta:
        verbose_name='برند'
        verbose_name_plural='برندها'

    def __str__(self):
        return f"({self.title})"

class Product(models.Model):
    title=models.CharField(max_length=300,verbose_name="عنوان")
    price=models.IntegerField(verbose_name="قیمت")
    image=models.ImageField(upload_to='images/products',null=True,blank=True,
    verbose_name='تصویر')
    short_description=models.CharField(max_length=300,null=True,verbose_name="توضیحات کوتاه")
    description=models.TextField(verbose_name="توضیحات")
    brand=models.ForeignKey(ProductBrand,on_delete=models.CASCADE,null=True,blank=True,
    verbose_name="برند")
    is_active=models.BooleanField(default=False,verbose_name="فعال/غیرفعال")
    is_delete=models.BooleanField(verbose_name="حذف")
    slug=models.SlugField(default="",null=False,db_index=True,blank=True, max_length=200,
    unique=True,verbose_name="slug")
    category=models.ManyToManyField(ProductCategory,related_name='products',
    verbose_name="دسته بندی")

    def get_absolute_url(self):
        return reverse('product-detail',args=[self.id])
    
    def __str__(self):
        return f'{self.title} ({self.price})'
    
    def save(self,*args,**kwargs):
        self.slug=slugify(self.title)
        super().save(*args,**kwargs)
    
    class Meta:
        verbose_name="محصول"
        verbose_name_plural="محصولات"

class ProductTag(models.Model):
     caption = models.CharField(max_length=300, db_index=True,verbose_name="کپشن")
     product = models.ForeignKey(Product, on_delete=models.CASCADE,
     related_name='product_tags',verbose_name="محصول")

     def __str__(self):
        return self.caption
    
     class Meta:
        verbose_name="تگ"
        verbose_name_plural="تگ ها"

class ProductVisit(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='محصول')
    ip=models.CharField(max_length=30,verbose_name='آپی کاربر')
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE,verbose_name='کاربر لاگین')
    
    def __str__(self):
        return f'{self.product.title} / {self.ip}'

    class Meta:
        verbose_name='بازدید محصول'
        verbose_name_plural='بازدیدهای محصول'

class ProductGallery(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='محصول')
    image=models.ImageField(upload_to='images/product_gallery')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name='تصویر گالری'
        verbose_name_plural='گالری تصاویر'
from django.db import models

# Create your models here.

class ContactUs(models.Model):
    title=models.CharField(max_length=300,verbose_name="عنوان")
    email=models.EmailField(max_length=300,verbose_name="ایمیل")
    full_name=models.CharField(max_length=300,verbose_name="نام و نام خانوادگی")
    message=models.TextField(verbose_name="پیام کاربر")
    created_date=models.DateTimeField(auto_now_add=True,verbose_name="تاریخ ایجاد")
    response=models.TextField(null=True,blank=True,verbose_name="پاسخ ادمین")
    is_read_by_admin=models.BooleanField(verbose_name="خوانده شده توسط ادمین",default=False)
    
    class Meta:
        verbose_name="پیام"
        verbose_name_plural="پیام ها"
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    image=models.ImageField(upload_to='images')
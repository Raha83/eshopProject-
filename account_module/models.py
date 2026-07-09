from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from django.contrib.auth import get_user_model

# Create your models here.

# user=get_user_model()

class User(AbstractUser):
    avatar=models.ImageField(upload_to='images/profile',blank=True,null=True,verbose_name='تصویر اواتار')
    email_active_code=models.CharField(max_length=100,blank=True,verbose_name="کد فعالسازی ایمیل")
    about_user=models.TextField(null=True,blank=True,verbose_name='درباره نویسنده')
    address=models.TextField(null=True,blank=True,verbose_name='آدرس')

    class Meta:
        verbose_name='کاربر'
        verbose_name_plural='کاربران'

    def __str__(self):
        if self.first_name is not '' and self.last_name is not '':
            return self.get_full_name()
        else:
            return self.email

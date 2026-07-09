from django.db import models
from account_module.models import User
from product_module.models import Product

# Create your models here.

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='کاربر')
    is_paid=models.BooleanField(verbose_name='پرداخت شده/نشده')
    paymentDate=models.DateField(null=True,blank=True,verbose_name='تاریخ پرداخت')
    
    def get_total_amount(self):
        total_amount=0
        if self.is_paid == True:
            for detail in self.orderdetail_set.all():
                total_amount += detail.final_price * detail.count
            return total_amount
        else:
            for detail in self.orderdetail_set.all():
                total_amount += detail.product.price * detail.count
            return total_amount

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name='سبد خرید'
        verbose_name_plural='سبد خرید کاربران'

class OrderDetail(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,verbose_name='سبد خرید')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='محصول')
    final_price=models.IntegerField(null=True,blank=True,verbose_name='قیمت نهایی تک محصول')
    count=models.IntegerField(verbose_name='تعداد محصول')

    def get_total_price(self):
        return self.count * self.product.price
        
    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name='جزییات سبد خرید'
        verbose_name_plural='لیست جزییات سبدهای خرید'
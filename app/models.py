from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
import uuid

def arabic_slugify(str):
    str = str.replace(" ", "-")
    str = str.replace(",", "-")
    str = str.replace("(", "-")
    str = str.replace(")", "")
    str = str.replace("؟", "")
    return str
# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=10000,error_messages ={ "unique":"عزيزي الموظف يوجد بالفعل منتج بهذا الاسم."} ,unique=True, verbose_name='اسم المنتج')
    content = models.TextField(null=True,blank=True, verbose_name=  'الوصف')
    image = models.ImageField(upload_to='Products',verbose_name='صورة المنتج')
    price = models.FloatField(default=0,verbose_name='سعر التاجير لمدة يوم')
    num_in_stock = models.IntegerField(default=0,verbose_name='العدد المتاح في المخزن')
    num_out_stock = models.IntegerField(default=0,verbose_name='العدد المستأجر')
    slug = models.SlugField(null=True,blank=True,unique=True,editable=False)
    active  = models.BooleanField(default=False,editable=False,verbose_name='موجود بالمخزن')
    date = models.DateTimeField(auto_now=True,editable=False)




    def __str__(self):
        a = str(self.title)
        return a

    def get_absolute_url(self):
        return f'/detail/{self.slug}'

    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            if not self.slug:
                self.slug = arabic_slugify(self.title)
        if self.num_in_stock > 0:
            self.active = True


        super(Product, self).save(*args, **kwargs)


    class Meta:
        ordering = ('-date',)
        verbose_name_plural = ('المنتجات')
        verbose_name = ('منتج')
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

class Order(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,unique=False,related_name='orders', verbose_name='المنتج')
    quantity = models.IntegerField(default=1,verbose_name='الكميه')
    date = models.DateTimeField(auto_now=True,editable=False)

    def __str__(self):
        a =str(self.quantity) +'  ' +str(self.product.title)
        return str(a)

    def clean(self):
        for b in Product.objects.filter(title = self.product.title):
            if self.quantity > b.num_in_stock:
                raise ValidationError({'quantity': ('هذه الكميه غير موجود بالمخزن حاليا. الكميه المتاحه بالمخزن هي ')+str(b.num_in_stock)})



    def save(self, *args, **kwargs):

        for b in Product.objects.filter(title = self.product.title):
            b.num_out_stock += self.quantity
            b.num_in_stock = b.num_in_stock - self.quantity
            b.save()





        super(Order, self).save(*args, **kwargs)
    class Meta:
        ordering = ('-date',)
        verbose_name_plural = ('المنتجات المستأجره')
        verbose_name = (' منتج مستاجر ')



class Rental(models.Model):
    product = models.ManyToManyField(Order,verbose_name='المنتج الذي سيتم تاجيره')
    time = models.IntegerField(verbose_name='مدة التاجير بالايام')
    from2 = models.DateField(default=timezone.now,verbose_name='تاريخ بداية التاجير')
    to = models.DateField(default=timezone.now,verbose_name='تاريخ نهاية التاجير')
    price = models.FloatField(default=0,verbose_name= 'اجمالي المبلغ المستحق')
    full_name = models.CharField(max_length=1000,verbose_name='اسم المستأجر ')
    email = models.EmailField(null=True,blank=True,verbose_name='البريد الالكتروني للمستأجر')
    phone = models.CharField(max_length=20,verbose_name='رقم هاتف المستاجر')
    address = models.TextField(verbose_name='عنوان التوصيل للمستاجر')
    content = models.TextField(null=True,blank=True, verbose_name=  'ملاحظات')
    active = models.BooleanField(default=True, verbose_name='عمليه جاريه')
    date = models.DateTimeField(auto_now=True,editable=False)

    def __str__(self):
        a = str(self.full_name)
        return a

    def get_absolute_url(self):
        return f'/pdf/{self.id}'

    def save(self, *args, **kwargs):
        super(Rental, self).save(*args, **kwargs)
    class Meta:
        ordering = ('-date',)
        verbose_name_plural = ('عمليات التأجير')
        verbose_name = ('عملية تأجير')


class OrderTow(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, unique=False, related_name='order',verbose_name='المنتج المطلوب')
    quantity = models.IntegerField(default=1, verbose_name='الكميه')
    time = models.IntegerField(verbose_name='مدة التاجير بالايام')
    price = models.IntegerField(default=0, verbose_name='المبلغ المستحق')
    full_name = models.CharField(max_length=1000, verbose_name='اسم المستأجر ')
    email = models.EmailField(null=True, blank=True, verbose_name='البريد الالكتروني ')
    phone = models.CharField(max_length=20, verbose_name='رقم الهاتف ')
    address = models.TextField(verbose_name='عنوان التوصيل ')
    content = models.TextField(null=True,blank=True, verbose_name=  'ملاحظات')
    date = models.DateTimeField(auto_now=True,editable=False,verbose_name='تاريخ الطلب')
    active = models.BooleanField(default=False,verbose_name='تم الدفع' ,editable=False)
    id = models.AutoField(primary_key=True ,verbose_name = 'رقم الطلب' ,editable=False)

    def __str__(self):
        a = str(self.full_name)
        return a
    def save(self, *args, **kwargs):
        for x in Product.objects.filter(id = self.product.id):
            self.price = x.price * self.quantity * self.time

        super(OrderTow, self).save(*args, **kwargs)
    class Meta:
        ordering = ('-date',)
        verbose_name_plural = ('الطلبات')
        verbose_name = ('طلب')













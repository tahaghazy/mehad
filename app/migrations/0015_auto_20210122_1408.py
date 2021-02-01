# Generated by Django 3.0.9 on 2021-01-22 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20210120_1514'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderr',
            options={'ordering': ('-start_date',), 'verbose_name': 'طلب', 'verbose_name_plural': 'الطلبات'},
        ),
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ('-timestamp',), 'verbose_name': 'تحويل مالي', 'verbose_name_plural': 'التحويلات الماليه'},
        ),
        migrations.RemoveField(
            model_name='rental',
            name='time',
        ),
        migrations.AddField(
            model_name='order',
            name='time',
            field=models.IntegerField(default=1, verbose_name='المده بالأيام'),
        ),
        migrations.AlterField(
            model_name='orderr',
            name='items',
            field=models.ManyToManyField(to='app.OrderTow', verbose_name='المنتجات المستأجره'),
        ),
        migrations.AlterField(
            model_name='orderr',
            name='label',
            field=models.CharField(choices=[('A', 'قيد الانتظار'), ('B', 'قيد المراجعه'), ('C', 'تم التسليم')], default='A', max_length=1, verbose_name='الحاله'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=100, verbose_name='البلغ المستحق'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='order_id',
            field=models.CharField(max_length=120, verbose_name='رقم الطلب'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='success',
            field=models.BooleanField(default=True, verbose_name='عمليه ناجحه'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاريخ العمليه'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='token',
            field=models.CharField(max_length=120, verbose_name='ID عملية الدفع'),
        ),
    ]

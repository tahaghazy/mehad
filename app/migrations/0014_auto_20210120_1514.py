# Generated by Django 3.0.9 on 2021-01-20 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20210120_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderr',
            name='id',
            field=models.AutoField(editable=False, primary_key=True, serialize=False, verbose_name='رقم الطلب'),
        ),
    ]
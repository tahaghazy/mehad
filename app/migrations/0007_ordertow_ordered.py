# Generated by Django 3.0.9 on 2021-01-18 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20210118_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordertow',
            name='ordered',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
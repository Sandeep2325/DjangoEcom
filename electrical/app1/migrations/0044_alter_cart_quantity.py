# Generated by Django 4.0.2 on 2022-05-21 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0043_product_specification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='Quantity'),
        ),
    ]

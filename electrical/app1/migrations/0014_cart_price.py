# Generated by Django 4.0.2 on 2022-03-19 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0013_remove_cart_complit_remove_cart_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Price(₹)'),
        ),
    ]

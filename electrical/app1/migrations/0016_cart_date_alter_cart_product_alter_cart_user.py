# Generated by Django 4.0.2 on 2022-03-19 05:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0015_remove_cart_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.product', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]

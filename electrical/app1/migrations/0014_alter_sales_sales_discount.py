# Generated by Django 4.0.2 on 2022-03-01 12:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0013_alter_customer_message_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='sales_discount',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)], verbose_name='Discount(%)'),
        ),
    ]

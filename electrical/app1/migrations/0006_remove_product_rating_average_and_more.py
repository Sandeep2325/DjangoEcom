# Generated by Django 4.0.2 on 2022-03-08 04:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_remove_product_avg_rating_product_rating_average_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='rating_average',
        ),
        migrations.RemoveField(
            model_name='product',
            name='review_count',
        ),
    ]

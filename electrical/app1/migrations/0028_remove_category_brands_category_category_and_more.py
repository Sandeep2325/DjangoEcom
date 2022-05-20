# Generated by Django 4.0.2 on 2022-04-06 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0027_orders_shipping_address_alter_socialmedialinks_links_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='brands',
        ),
        migrations.AddField(
            model_name='category',
            name='category',
            field=models.CharField(max_length=50, null=True, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Category Description'),
        ),
    ]
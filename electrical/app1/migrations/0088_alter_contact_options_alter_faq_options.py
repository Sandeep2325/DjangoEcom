# Generated by Django 4.0.2 on 2022-02-25 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0087_alter_rating_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'verbose_name_plural': 'Customer messages'},
        ),
        migrations.AlterModelOptions(
            name='faq',
            options={'verbose_name_plural': 'FAQs'},
        ),
    ]

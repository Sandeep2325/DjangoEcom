# Generated by Django 4.0.2 on 2022-02-25 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0092_blog_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]

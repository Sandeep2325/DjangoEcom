# Generated by Django 4.0.2 on 2022-02-23 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0079_alter_blog_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='Banner'),
        ),
    ]

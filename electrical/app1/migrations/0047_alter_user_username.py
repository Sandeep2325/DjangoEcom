# Generated by Django 4.0.2 on 2022-05-26 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0046_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=50, null=True, verbose_name='Full name'),
        ),
    ]

# Generated by Django 4.0.2 on 2022-02-26 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0097_alter_rating_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='Status',
            field=models.CharField(choices=[('Reject', 'Reject'), ('Approve', 'Approved')], max_length=8),
        ),
    ]

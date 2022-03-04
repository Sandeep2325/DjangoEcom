# Generated by Django 4.0.2 on 2022-03-04 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0027_delete_mail_alter_mailtext_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailtext',
            name='message',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mailtext',
            name='subject',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.RemoveField(
            model_name='mailtext',
            name='users',
        ),
        migrations.AddField(
            model_name='mailtext',
            name='users',
            field=models.CharField(max_length=255, null=True),
        ),
    ]

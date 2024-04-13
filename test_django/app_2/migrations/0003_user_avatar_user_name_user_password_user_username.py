# Generated by Django 5.0.4 on 2024-04-13 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_2', '0002_rename_job_task_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default=None, upload_to='product_images/'),
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]

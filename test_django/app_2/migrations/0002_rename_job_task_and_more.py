# Generated by Django 5.0.4 on 2024-04-12 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_2', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Job',
            new_name='Task',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='date_create_job',
            new_name='date_create_task',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='description_job',
            new_name='description_task',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='id_job',
            new_name='id_task',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='name_job',
            new_name='name_task',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='jobs',
            new_name='tasks',
        ),
    ]

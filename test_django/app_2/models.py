from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='product_images/', null=False, default=None)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=100, blank=True)
    school = models.CharField(max_length=100, blank=True)
    tasks = models.ManyToManyField('Task', related_name='users', blank=True)

class Task(models.Model):
    id_task = models.AutoField(primary_key=True)
    name_task = models.CharField(max_length=100)
    description_task = models.CharField(max_length=500)
    date_create_task = models.DateField(null=True, blank=True)
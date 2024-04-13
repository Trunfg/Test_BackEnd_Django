from rest_framework import serializers
from app_2.models import User, Task

class taskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id_task","name_task", "description_task", "date_create_task"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "username", "password", "avatar", "address", "school", "date_of_birth"]
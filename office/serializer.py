from rest_framework import serializers
from office.models import Office, Task


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ['name', 'address']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['task']

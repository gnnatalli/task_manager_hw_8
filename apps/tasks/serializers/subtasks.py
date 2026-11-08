from rest_framework.serializers import ModelSerializer, DateTimeField

from apps.tasks.models import SubTask


class SubTaskSerializer(ModelSerializer):

    class Meta:
        model = SubTask
        fields = '__all__'


class SubTaskCreateSerializer(ModelSerializer):
    created_at = DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = '__all__'

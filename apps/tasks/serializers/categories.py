from rest_framework.serializers import ModelSerializer, CharField, ValidationError

from apps.tasks.models import Category


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class CategoryCreateSerializer(ModelSerializer):
    # Отключаем автоматическую проверку unique,
    # потому что реализуем собственную проверку в create и update.
    name = CharField(validators=[])

    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        name = validated_data.get('name')

        if Category.objects.filter(name=name).exists():
            raise ValidationError({'name': 'Такая категория уже существует.'})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get('name', instance.name)

        if Category.objects.filter(name=name).exclude(pk=instance.pk).exists():
            raise ValidationError(
                {'name': 'Такая категория уже существует.'}
            )
        return super().update(instance, validated_data)

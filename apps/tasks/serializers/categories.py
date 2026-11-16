from rest_framework.serializers import ModelSerializer, CharField, ValidationError

from apps.tasks.models import Category


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('is_deleted', 'deleted_at')


class CategoryCreateSerializer(ModelSerializer):
    # Отключаем автоматическую проверку unique,
    # потому что реализуем собственную проверку в create и update.
    name = CharField(validators=[])

    class Meta:
        model = Category
        fields = ['id', 'name', 'is_deleted', 'deleted_at']
        read_only_fields = ('id', 'is_deleted', 'deleted_at')


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

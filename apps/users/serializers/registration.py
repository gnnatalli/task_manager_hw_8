from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    # Пароль доступен только для записи
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    # Email обязателен
    email = serializers.EmailField(
        required=True,
        allow_blank=False
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def validate_username(self, value):
        # Проверяем уникальность логина
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким логином уже существует.'
            )
        return value

    def validate_email(self, value):
        # Проверяем уникальность email без учёта регистра
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.'
            )
        return value

    def validate(self, attrs):
        # Проверяем сложность пароля с учётом данных пользователя
        user = User(
            username=attrs['username'],
            email=attrs['email']
        )
        validate_password(attrs['password'], user=user)
        return attrs

    def create(self, validated_data):
        # create_user автоматически хэширует пароль
        return User.objects.create_user(**validated_data)

    # required=True — email обязательно должен быть передан.
    # validate_username() — проверяет уникальность логина.
    # validate_email() — проверяет уникальность email.
    # validate_password() — проверяет сложность пароля с учётом данных пользователя.
    # create_user() — сохраняет пароль в хэшированном виде.
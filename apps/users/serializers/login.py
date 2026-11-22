from django.contrib.auth import authenticate
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True
    )

    def validate(self, attrs):
        # Проверяем логин и пароль
        user = authenticate(
            request=self.context.get('request'),
            username=attrs['username'],
            password=attrs['password']
        )

        if not user:
            raise serializers.ValidationError(
                'Неверный логин или пароль.'
            )

        # Сохраняем найденного пользователя
        attrs['user'] = user
        return attrs

    # authenticate() проверяет логин и пароль по данным в базе.
    # Если данные неправильные, возвращается ошибка.
    # write_only=True защищает пароль от попадания в ответ API.
    # attrs['user'] передаёт найденного пользователя дальше в представление.
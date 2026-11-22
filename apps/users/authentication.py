from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        # Получаем Access Token из Cookie
        raw_token = request.COOKIES.get('access_token')

        # Если Cookie отсутствует, используем стандартный способ
        if raw_token is None:
            return super().authenticate(request)

        # Игнорируем пустую Cookie после выхода из системы
        if raw_token.strip() in ('', '""', "''"):
            return None

        # Проверяем токен и получаем пользователя
        validated_token = self.get_validated_token(
            raw_token.encode('utf-8')
        )

        return self.get_user(validated_token), validated_token
    # request.COOKIES — получает токены из Cookies.
    # get_validated_token() — проверяет подлинность и срок действия токена.
    # get_user() — определяет пользователя по токену.
    # JWTAuthentication — базовый класс SimpleJWT, который мы расширяем.
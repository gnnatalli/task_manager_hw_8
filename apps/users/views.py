from django.conf import settings

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from apps.users.serializers.registration import RegistrationSerializer
from apps.users.serializers.login import LoginSerializer


class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    # CreateAPIView — готовое представление DRF для создания объектов через POST.
    # AllowAny — разрешает регистрацию даже неавторизованным пользователям.
    # serializer_class — указывает, какие данные и как проверять.

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        # Создаём пару JWT-токенов
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        response = Response({
            'message': 'Вход выполнен успешно.',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        }, status=status.HTTP_200_OK)

        # Сохраняем access в HttpOnly cookie
        response.set_cookie(
            'access_token',
            str(access),
            max_age=int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax',
            path='/',
        )

        # Сохраняем refresh в HttpOnly cookie
        response.set_cookie(
            'refresh_token',
            str(refresh),
            max_age=int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax',
            path='/',
        )

        return response

# RefreshToken.for_user(user) создаёт refresh-токен.
# refresh.access_token создаёт access-токен.
# httponly=True запрещает JavaScript читать cookie.
# secure=not settings.DEBUG требует HTTPS вне режима разработки.


class CookieTokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Получаем Refresh Token из Cookie
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response(
                {'detail': 'Refresh token отсутствует.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Проверяем Refresh Token и создаём новые токены
        serializer = TokenRefreshSerializer(
            data={'refresh': refresh_token}
        )

        try:
            serializer.is_valid(raise_exception=True)
        except (TokenError, InvalidToken):
            response = Response(
                {'detail': 'Refresh token недействителен.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
            response.delete_cookie('access_token', path='/')
            response.delete_cookie('refresh_token', path='/')
            return response

        data = serializer.validated_data

        response = Response(
            {'message': 'Токены успешно обновлены.'},
            status=status.HTTP_200_OK
        )

        # Сохраняем новый Access Token
        response.set_cookie(
            'access_token',
            data['access'],
            max_age=int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax',
            path='/',
        )

        # При включённой ротации сохраняем новый Refresh Token
        if 'refresh' in data:
            response.set_cookie(
                'refresh_token',
                data['refresh'],
                max_age=int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                path='/',
            )

        return response

    # request.COOKIES — получает токен из Cookies.
    # TokenRefreshSerializer — проверяет Refresh Token и обновляет токены.
    # set_cookie() — сохраняет новые токены в браузере или Postman.
    # BLACKLIST_AFTER_ROTATION=True — старый Refresh Token становится недействительным после ротации.

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Получаем Refresh Token из Cookie
        refresh_token = request.COOKIES.get('refresh_token')

        # Отзываем Refresh Token
        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except TokenError:
                pass

        # Удаляем токены из Cookies
        response = Response(
            {'message': 'Выход выполнен успешно.'},
            status=status.HTTP_200_OK
        )

        response.delete_cookie('access_token', path='/', samesite='Lax')
        response.delete_cookie('refresh_token', path='/', samesite='Lax')

        return response
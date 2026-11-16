import logging

# Получаем логгер для HTTP-запросов
logger = logging.getLogger('http')


class HTTPRequestLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Записываем метод, адрес и HTTP-статус ответа
        logger.info(
            '%s %s %s',
            request.method,
            request.get_full_path(),
            response.status_code,
        )

        return response
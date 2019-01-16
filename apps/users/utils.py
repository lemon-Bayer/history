from .models import User
from django_redis import get_redis_connection


def perform_authentication(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    conn = get_redis_connection('session')
    username = conn.get('username_%s' % token)
    user_token = conn.get('token_%s' % token)
    user = User.objects.get(username=username)
    if token == user_token.decode():
        return user





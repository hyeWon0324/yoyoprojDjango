from django.core.cache import cache
from django.http import Http404, JsonResponse
from django.conf import settings
from rest_framework.response import Response
import jwt
import re
from .models import Users


class MyTokenAuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        access_token = request.cookies.get("access_token")

        if access_token is not None:
            payload = jwt.decode(access_token, 'HS256')
            user_idx = payload['idx']  # user_id, idx, email
            user = Users.objects.get(idx=user_idx)
            request.user = user

        response = self.get_response(request)
        response.set_cookie('access_token', access_token)

        return response

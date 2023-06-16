from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.conf import settings
import jwt


class JwtLoginMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if token := request.COOKIES.get('jwt'):
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload.get('user_id')
                if user_id:
                    user = get_user_model().objects.get(pk=user_id)
                    if str(user.pk) == str(kwargs.get('pk')):
                        request.user = user
                        return super().dispatch(request, *args, **kwargs)
                    else:
                        url = reverse('auth:login')
                        response = HttpResponseRedirect(url)
                        return response
                else:
                    return HttpResponse('User not found.', status=401)
            except jwt.ExpiredSignatureError:
                return HttpResponse('JWT token has expired.', status=401)
            except jwt.InvalidTokenError:
                return HttpResponse('Invalid JWT token.', status=401)
        else:
            url = reverse('auth:login')
            response = HttpResponseRedirect(url)
            return response

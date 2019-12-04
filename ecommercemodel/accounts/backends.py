from django.contrib.auth.backends import ModelBackend as BaseModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(BaseModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username is None:
            try:
                user = User.objects.get(email=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                pass
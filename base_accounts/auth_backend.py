from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailBackend(ModelBackend):

    def authenticate(self, email=None, password=None):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email__iexact=email.lower())
            if user.check_password(password):
                return user
        except user_model.DoesNotExist:
            return None

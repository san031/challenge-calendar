from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

#ModelBackend authenticates against settings.AUTH_USER_MODEL

class EmailBackend(ModelBackend):
    def authenticate(self, request, username = None, password = None, **kwargs):
        UserModel = get_user_model
        try:
            user = UserModel.model.object.get(email = username)
        except UserModel.DoesnotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
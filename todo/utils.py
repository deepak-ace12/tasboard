from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.mail import EmailMessage


class EmailBackend(ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            UserModel.USERNAME_FIELD = 'email'
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if (user.check_password(password) and
                    self.user_can_authenticate(user)):
                return user


def send_mail(subject, body, to):
    email = EmailMessage(subject=subject, body=body, to=[to])
    email.send()

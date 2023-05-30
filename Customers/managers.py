from django.contrib.auth.models import BaseUserManager


class CustomerManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        username = self.username(username)
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)

        user.set_password(password)
        user.save()

        return user

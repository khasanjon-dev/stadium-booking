from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import TextChoices, CharField

from utils.validators import phone_regex


class UserManager(BaseUserManager):

    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('Users must have a phone number!')

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        user = self.create_user(phone, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    class Role(TextChoices):
        OWNER = 'owner', 'owner'
        USER = 'user', 'user'

    name = CharField(max_length=250)
    username = CharField(max_length=150, blank=True, null=True)
    phone = CharField(max_length=12, validators=[phone_regex], unique=True)
    role = CharField(max_length=5, choices=Role.choices)
    objects = UserManager()

    USERNAME_FIELD = 'phone'

    class Meta:
        ordering = ['-id']

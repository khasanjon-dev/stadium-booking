from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer, Serializer, CharField

from users.models import User


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'phone', 'role', 'id', 'password')

    def validate(self, attrs):
        if password := attrs.get('password'):
            attrs['password'] = make_password(password)
        return attrs


class RegisterSerializer(Serializer):
    phone = CharField()
    name = CharField()
    password = CharField()
    role = CharField()

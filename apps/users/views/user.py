from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from users.models import User
from users.serializers import UserModelSerializer


class UserViewSet(GenericViewSet, CreateModelMixin, ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


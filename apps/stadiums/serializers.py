from rest_framework.fields import HiddenField, CurrentUserDefault
from rest_framework.serializers import ModelSerializer

from stadiums.models import Stadium


class StadiumModelSerializer(ModelSerializer):
    owner = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Stadium
        fields = '__all__'

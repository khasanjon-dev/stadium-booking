from datetime import datetime

from rest_framework.exceptions import ValidationError
from rest_framework.fields import HiddenField, CurrentUserDefault
from rest_framework.serializers import ModelSerializer, Serializer, DateTimeField, FloatField

from stadiums.models import Stadium
from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'phone')


class StadiumModelSerializer(ModelSerializer):
    owner = UserSerializer(HiddenField(default=CurrentUserDefault()))

    class Meta:
        model = Stadium
        fields = '__all__'


class FreeStadiumSerializer(Serializer):
    start = DateTimeField()
    end = DateTimeField()

    def validated_data(self):
        start = self.start
        end = self.end
        _range = (start, end)
        _start = start.strftime('%Y-%m-%d %H:%M')
        _end = end.strftime('%Y-%m-%d %H:%M')
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M')
        if _start <= date_now or _start >= _end or _end <= date_now:
            raise ValidationError("Sana vaqt xato kiritilgan!")


class NearStadiumSerializer(Serializer):
    longitude = FloatField()
    latitude = FloatField()

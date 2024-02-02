from datetime import datetime

from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, CurrentUserDefault, HiddenField

from stadiums.serializers import StadiumModelSerializer
from users.models import Booking


class BookingModelSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Booking
        fields = '__all__'


class BookingCreateSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    def validate(self, attrs):
        start = attrs.get('start')
        end = attrs.get('end')
        _range = (start, end)
        _start = start.strftime('%Y-%m-%d %H:%M')
        _end = end.strftime('%Y-%m-%d %H:%M')
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M')
        if _start <= date_now or _start >= _end or _end <= date_now:
            raise ValidationError("Sana vaqt xato kiritilgan!")
        if Booking.objects.filter(Q(start__range=_range) | Q(end__range=_range)).exists():
            raise ValidationError("Bu vaqtda maydon bo'sh emas!")
        return super().validate(attrs)

    class Meta:
        model = Booking
        fields = '__all__'


class BookStadiumSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    stadium = StadiumModelSerializer(required=False)

    class Meta:
        model = Booking
        fields = '__all__'



from rest_framework.fields import CurrentUserDefault, HiddenField
from rest_framework.serializers import ModelSerializer

from users.models import Booking


class BookingModelSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Booking
        fields = '__all__'

from django.db.models import Model, CharField, FloatField, IntegerField, ImageField, ForeignKey, CASCADE, F, \
    ExpressionWrapper
from django.db.models.functions import Radians, ACos, Sin, Cos

from users.models import User
from utils.validators import phone_regex


class Stadium(Model):
    name = CharField(max_length=300)
    # contact
    contact = CharField(max_length=12, validators=[phone_regex])
    price = IntegerField()
    photo = ImageField(upload_to='stadiums/photos/')
    # address
    latitude = FloatField()
    longitude = FloatField()
    # relationship
    owner = ForeignKey(User, CASCADE, 'stadiums')

    @staticmethod
    def haversine_distance(latitude, longitude):
        lat_diff = Radians(F('latitude') - latitude)
        lon_diff = Radians(F('longitude') - longitude)
        a = ACos(
            Sin(lat_diff / 2) ** 2 + Cos(Radians(latitude)) * Cos(Radians(F('latitude'))) * Sin(lon_diff / 2) ** 2)
        distance_expression = ExpressionWrapper(a * 6371, output_field=FloatField())
        return distance_expression

    @classmethod
    def get_nearest_stadium(self, latitude, longitude):
        stadiums = Stadium.objects.annotate(distance=self.haversine_distance(latitude, longitude))
        sorted_stadiums = stadiums.order_by('-distance')
        return sorted_stadiums

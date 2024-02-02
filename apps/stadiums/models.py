from django.db.models import Model, CharField, FloatField, IntegerField, ImageField, ForeignKey, CASCADE

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

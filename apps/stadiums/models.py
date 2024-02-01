from django.db.models import Model, CharField, FloatField, IntegerField, ImageField, ForeignKey, CASCADE

from users.models import User


class Stadium(Model):
    name = CharField(max_length=300)
    # contact
    phone = CharField(max_length=100)
    price = IntegerField()
    photo = ImageField(upload_to='stadiums/photos/')
    # address
    latitude = FloatField()
    longitude = FloatField()
    # relationship
    owner = ForeignKey(User, CASCADE, 'stadiums')

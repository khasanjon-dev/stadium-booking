from django.db.models import Model, ForeignKey, CASCADE, DateTimeField

from stadiums.models import Stadium
from users.models import User


class Booking(Model):
    # date
    start = DateTimeField()
    end = DateTimeField()
    # relationship
    stadium = ForeignKey(Stadium, CASCADE)
    user = ForeignKey(User, CASCADE)

    class Meta:
        ordering = ('start',)

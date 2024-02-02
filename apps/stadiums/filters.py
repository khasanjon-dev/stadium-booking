from django_filters import FilterSet

from stadiums.models import Stadium


class StadiumFilter(FilterSet):
    class Meta:
        model = Stadium
        fields = {
            ''
        }
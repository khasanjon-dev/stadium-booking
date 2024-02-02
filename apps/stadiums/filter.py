from django_filters import FilterSet, DateTimeFilter, CharFilter

from stadiums.models import Stadium


class StadiumFilter(FilterSet):
    start = DateTimeFilter()
    end = DateTimeFilter()
    latitude = CharFilter()
    longitude = CharFilter()

    # class Meta:
    #     model = Stadium
    #     fields = ('latitude', 'longitude', 'start', 'end')

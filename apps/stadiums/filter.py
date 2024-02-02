from django_filters import FilterSet, DateTimeFilter

from stadiums.models import Stadium


class StadiumFilter(FilterSet):
    start = DateTimeFilter()
    end = DateTimeFilter()

    # latitude = NumericRangeFilter()
    # longitude = NumericRangeFilter()

    class Meta:
        model = Stadium
        fields = ('latitude', 'longitude', 'start', 'end')

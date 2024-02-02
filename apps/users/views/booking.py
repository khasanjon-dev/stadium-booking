from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from stadiums.models import Stadium
from users.models import Booking
from users.serializers import BookingModelSerializer, BookStadiumSerializer
from users.serializers.booking import BookingCreateSerializer


class BookingViewSet(GenericViewSet, CreateModelMixin):
    queryset = Booking.objects.all()
    serializer_class = BookingModelSerializer
    permission_classes = (IsAuthenticated,)

    @action(['POST'], False, 'create', serializer_class=BookingCreateSerializer)
    def book(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        context = {
            "error": "Uzr, siz tanlagan vaqtda maydon band!"
        }
        return Response(context, status.HTTP_410_GONE)

    @action(['get'], False, 'get-book-stadium', serializer_class=BookStadiumSerializer)
    def get_book_stadium(self, request):
        '''
        ownerning aynan bitta stadioni band qilingan vaqtlarni ko'rsatadi
        '''
        queryset = Booking.objects.filter(stadium__owner=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



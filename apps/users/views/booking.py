from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from users.models import Booking
from users.serializers import BookingModelSerializer


class BookingViewSet(GenericViewSet, CreateModelMixin):
    queryset = Booking.objects.all()
    serializer_class = BookingModelSerializer
    permission_classes = (IsAuthenticated,)


    @action(['POST'], detail=True, serializer_class=BookingModelSerializer)
    def book(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(room_id=pk)
            response = {
                "message": "xona muvaffaqiyatli band qilindi"
            }
            return Response(response, status.HTTP_201_CREATED)
        response = {
            "error": "uzr, siz tanlagan vaqtda xona band"
        }
        return Response(response, status.HTTP_410_GONE)
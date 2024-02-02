from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from stadiums.filter import StadiumFilter
from stadiums.models import Stadium
from stadiums.serializers import StadiumModelSerializer, FreeStadiumSerializer, NearStadiumSerializer
from utils.permissions import IsUserOwnerOrAdmin


class StadiumViewSet(ModelViewSet):
    queryset = Stadium.objects.all()
    serializer_class = StadiumModelSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = StadiumFilter

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        start = request.query_params.get('start', None)
        end = request.query_params.get('end', None)
        latitude = request.query_params.get('latitude', None)
        longitude = request.query_params.get('longitude', None)
        if start and end:
            stadiums = Stadium.objects.filter(
                ~Q(Q(booking__start__gt=start, booking__end__lte=start) | Q(booking__start__gt=end,
                                                                            booking__end__lte=end)))
            if stadiums:
                serializer = StadiumModelSerializer(stadiums, many=True)
                return Response(serializer.data)
            context = {'message': "Bu vatqga bo'sh maydon yo'q!"}
            return Response(context, 404)
        if latitude and longitude:
            nearest_stadiums = Stadium.get_nearest_stadium(latitude, longitude)
            serializer = StadiumModelSerializer(nearest_stadiums, many=True)
            return Response(serializer.data)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):

        queryset = super().get_queryset()
        if self.action in ('list', 'retrieve'):
            return queryset
        if self.request.user.is_authenticated:
            return queryset.filter(owner=self.request.user)

    @action(['get'], False, 'stadiums', permission_classes=(IsUserOwnerOrAdmin,))
    def get_stadiums(self, reqeust):
        '''
        ownerni stadiumlarni olish

        ```
        ```
        '''
        queryset = self.queryset.filter(owner=reqeust.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # @action(['post'], False, 'free', serializer_class=FreeStadiumSerializer,
    #         permission_classes=(AllowAny,))
    # def get_free_stadiums(self, request):
    #     # serializer = self.get_serializer(request.data)
    #     start = request.GET.get('start')
    #     end = request.GET.get('end')
    #     stadiums = Stadium.objects.filter(
    #         ~Q(Q(booking__start__gt=start, booking__end__lte=start) | Q(booking__start__gt=end, booking__end__lte=end)))
    #     if stadiums:
    #         serializer = StadiumModelSerializer(stadiums, many=True)
    #         return Response(serializer.data)
    #     context = {'message': "Bu vatqga bo'sh maydon yo'q!"}
    #     return Response(context, 404)
    #
    # @action(['post'], False, 'near', serializer_class=NearStadiumSerializer, permission_classes=(AllowAny,))
    # def get_near_stadium(self, request):
    #     '''
    #     eng yaqin stadiumni olish
    #     '''
    #
    #     serializer = self.get_serializer(request.data)
    #     longitude = serializer.data.get('longitude')
    #     latitude = serializer.data.get('latitude')
    #
    #     nearest_stadiums = Stadium.get_nearest_stadium(latitude, longitude)
    #     serializer = StadiumModelSerializer(nearest_stadiums, many=True)
    #     return Response(serializer.data)

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from stadiums.models import Stadium
from stadiums.serializers import StadiumModelSerializer
from utils.permissions import IsUserOwnerOrAdmin


class CustomListModelMixin:

    def list(self, request, *args, **kwargs):
        '''
        owner ga tegishli stadionlar

        ```
        ```
        '''
        queryset = self.filter_queryset(Stadium.objects.filter(owner=request.user))
        if request.user.is_staff:
            queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CustomUpdateModelMixin(UpdateModelMixin):
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if not Stadium.objects.filter(id=instance.id, owner=request.user).exists() or not request.user.is_staff:
            context = {'message': 'It is not your stadium!'}
            return Response(context, status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class CustomDestroyModelMixin(DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not Stadium.objects.filter(id=instance.id, owner=request.user).exists() or not request.user.is_staff:
            context = {'message': 'It is not your stadium!'}
            return Response(context, status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class StadiumViewSet(GenericViewSet, CreateModelMixin, CustomListModelMixin, CustomUpdateModelMixin,
                     CustomDestroyModelMixin):
    queryset = Stadium.objects.all()
    serializer_class = StadiumModelSerializer
    permission_classes = (IsAuthenticated, IsUserOwnerOrAdmin)

    @action(['get'], False, 'stadiums', permission_classes=(AllowAny,))
    def get_stadiums(self, reqeust):
        '''
        barcha stadiumlarni olish

        ```
        ```
        '''
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

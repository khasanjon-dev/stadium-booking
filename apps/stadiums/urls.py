from django.urls import path, include
from rest_framework.routers import DefaultRouter

from stadiums.views import StadiumViewSet

router = DefaultRouter()
router.register('', StadiumViewSet, 'stadium')

urlpatterns = [
    path('', include(router.urls))
]

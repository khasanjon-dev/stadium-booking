from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views.booking import BookingViewSet
from users.views.user import UserViewSet

router = DefaultRouter()
router.register('', UserViewSet, 'users')
router.register('booking', BookingViewSet, 'booking')

urlpatterns = [
    path('', include(router.urls)),
    path('access/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
]

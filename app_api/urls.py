from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import DestinationViewSet, BookingViewSet, ReviewViewSet
from .jwt_views import CustomTokenObtainPairView


router = DefaultRouter()
router.register('destinations', DestinationViewSet, basename='destinations')
router.register('bookings', BookingViewSet, basename='bookings')
router.register('reviews', ReviewViewSet, basename='reviews')


urlpatterns = [
    path('', include(router.urls)),

    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
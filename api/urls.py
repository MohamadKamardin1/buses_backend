from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    RouteViewSet, StationViewSet, BusViewSet, BookingViewSet, RegisterView,
    MyTokenObtainPairView
)
# Add this import:
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'routes', RouteViewSet)
router.register(r'stations', StationViewSet)
router.register(r'buses', BusViewSet)
router.register(r'bookings', BookingViewSet) # Assuming you've already fixed the queryset issue here

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Change this line:
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]

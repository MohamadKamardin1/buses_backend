from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Route, Station, Bus, Booking, Seat
from .serializers import (
    UserSerializer, RouteSerializer, StationSerializer, BusSerializer,
    BookingSerializer, SeatSerializer, RegisterSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Custom JWT token to include user role in payload
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# User registration
from rest_framework import generics
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]

class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = [IsAuthenticated]

class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def update_location(self, request, pk=None):
        bus = self.get_object()
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        if latitude is None or longitude is None:
            return Response({'detail': 'Latitude and longitude required.'}, status=status.HTTP_400_BAD_REQUEST)
        bus.latitude = latitude
        bus.longitude = longitude
        bus.save()
        return Response(self.get_serializer(bus).data)

    @action(detail=True, methods=['post'])
    def update_passenger_count(self, request, pk=None):
        bus = self.get_object()
        count = request.data.get('passenger_count')
        if count is None:
            return Response({'detail': 'Passenger count required.'}, status=status.HTTP_400_BAD_REQUEST)
        bus.passenger_count = count
        bus.save()
        return Response(self.get_serializer(bus).data)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'traveler':
            return Booking.objects.filter(traveler=user)
        # Admin sees all; conductor maybe none or filtered by buses
        return Booking.objects.all()

# Optional Seat ViewSet if you separate seat management
class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [IsAuthenticated]

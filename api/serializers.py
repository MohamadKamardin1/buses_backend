from rest_framework import serializers
from .models import User, Route, Station, Bus, Booking, Seat

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone', 'first_name', 'last_name']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'phone', 'first_name', 'last_name']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ['id', 'route', 'name', 'order', 'latitude', 'longitude']

class RouteSerializer(serializers.ModelSerializer):
    stations = StationSerializer(many=True, read_only=True)
    class Meta:
        model = Route
        fields = ['id', 'name', 'from_location', 'to_location', 'stations']

class BusSerializer(serializers.ModelSerializer):
    route = RouteSerializer(read_only=True)
    route_id = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all(), source='route', write_only=True)
    current_station = StationSerializer(read_only=True)
    current_station_id = serializers.PrimaryKeyRelatedField(queryset=Station.objects.all(), source='current_station', write_only=True, allow_null=True)
    conductor = UserSerializer(read_only=True)
    conductor_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='conductor'), source='conductor', write_only=True, allow_null=True)

    class Meta:
        model = Bus
        fields = [
            'id', 'plate_number', 'route', 'route_id', 'total_seats', 'status', 
            'current_station', 'current_station_id', 'conductor', 'conductor_id',
            'latitude', 'longitude', 'passenger_count'
        ]

class BookingSerializer(serializers.ModelSerializer):
    traveler = UserSerializer(read_only=True)
    bus = BusSerializer(read_only=True)
    bus_id = serializers.PrimaryKeyRelatedField(queryset=Bus.objects.all(), source='bus', write_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'traveler', 'bus', 'bus_id', 'seats', 'passengers', 
            'luggage_count', 'total_price', 'status', 'booked_at'
        ]
        read_only_fields = ['status', 'booked_at']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['traveler'] = user
        return super().create(validated_data)

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'bus', 'seat_number', 'is_booked', 'is_premium']

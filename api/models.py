from django.contrib.auth.models import AbstractUser
from django.db import models

# User model with roles
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('conductor', 'Conductor'),
        ('traveler', 'Traveler'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class Route(models.Model):
    name = models.CharField(max_length=100)
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Station(models.Model):
    route = models.ForeignKey(Route, related_name='stations', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        unique_together = ('route', 'order')
        ordering = ['order']

    def __str__(self):
        return f"{self.name} (Route: {self.route.name})"

class Bus(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Maintenance'),
    )
    plate_number = models.CharField(max_length=20, unique=True)
    route = models.ForeignKey(Route, related_name='buses', on_delete=models.SET_NULL, null=True)
    total_seats = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    current_station = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True, blank=True)
    conductor = models.ForeignKey(User, limit_choices_to={'role': 'conductor'}, on_delete=models.SET_NULL, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    passenger_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.plate_number} ({self.route.name if self.route else 'No Route'})"

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    traveler = models.ForeignKey(User, limit_choices_to={'role': 'traveler'}, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seats = models.JSONField(default=list)  # List of seat numbers
    passengers = models.PositiveIntegerField()
    luggage_count = models.PositiveIntegerField(default=0)
    total_price = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id} for {self.traveler.username} on {self.bus.plate_number}"

# Optional: If you want seats as separate entities per bus
class Seat(models.Model):
    bus = models.ForeignKey(Bus, related_name='seats', on_delete=models.CASCADE)
    seat_number = models.PositiveIntegerField()
    is_booked = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)

    class Meta:
        unique_together = ('bus', 'seat_number')

    def __str__(self):
        return f"Seat {self.seat_number} on Bus {self.bus.plate_number}"

from django.contrib import admin
from .models import User, Route, Station, Bus, Booking, Seat

admin.site.register(User)
admin.site.register(Route)
admin.site.register(Station)
admin.site.register(Bus)
admin.site.register(Booking)
admin.site.register(Seat)

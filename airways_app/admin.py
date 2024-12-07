from django.contrib import admin
from django.contrib.auth.models import User
from .models import Appointment
from .models import Register
from .models import Booking

# Register your models here.
admin.site.register(Appointment)

admin.site.register(Register)

admin.site.register(Booking)
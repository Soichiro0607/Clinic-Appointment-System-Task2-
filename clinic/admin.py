from django.contrib import admin
from .models import Doctor, AppointmentSlot, Appointment

admin.site.register(Doctor)
admin.site.register(AppointmentSlot)
admin.site.register(Appointment)
from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    SPECIALTY_CHOICES = [
        ('GP', 'General Practice'),
        ('SUR', 'Surgery'),
        ('PED', 'Pediatrics'),
        ('CAR', 'Cardiology'),
        ('DER', 'Dermatology'),
    ]
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=50, choices=SPECIALTY_CHOICES)

    def __str__(self):
        return self.name


class AppointmentSlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doctor} - {self.date} {self.time}"


class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.OneToOneField(AppointmentSlot, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.patient} - {self.slot}"
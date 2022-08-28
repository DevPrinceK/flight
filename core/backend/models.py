import time
import string
import random
from django.db import models

from accounts.models import User


class Agency(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name if self.name else "agency"

    class Meta:
        db_table = 'agency'


class Vehicle(models.Model):
    name = models.CharField(max_length=255)
    vin = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey('VehicleCategory', on_delete=models.CASCADE, null=True, blank=True)  # noqa
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, null=True, blank=True)  # noqa
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name if self.name else "vehicle"

    class Meta:
        db_table = 'vehicle'


class Seat(models.Model):
    seat_num = models.IntegerField(default=1)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True, blank=True)  # noqa
    is_booked = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.seat_num) if str(self.seat_num) else "seat"

    class Meta:
        db_table = 'seat'


class VehicleCategory(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name if self.name else "category"

    class Meta:
        db_table = 'category'


class Trip(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True, blank=True)  # noqa
    source = models.CharField(max_length=255, null=True, blank=True)
    destination = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.source + "-" + self.destination if self.source and self.destination else "trip"  # noqa

    class Meta:
        db_table = 'trip'


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # noqa
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, null=True, blank=True)  # noqa
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, null=True, blank=True)  # noqa
    date = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email if self.user.email else "booking"

    class Meta:
        db_table = 'booking'


class Ticket(models.Model):
    def generate_ticket_id():
        time_id = str(int(time.time() * 1000))
        return time_id.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    ticket_id = models.CharField(max_length=255, null=True, blank=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)  # noqa
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE, null=True, blank=True)  # noqa
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.seat if self.seat else "ticket"

    class Meta:
        db_table = 'ticket'


class Transaction(models.Model):
    def generate_transaction_id():
        time_id = str(int(time.time() * 100))
        return time_id.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    external_id = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    network = models.CharField(max_length=255, null=True, blank=True)
    status_code = models.CharField(max_length=255, null=True, blank=True)
    status_message = models.CharField(max_length=255, null=True, blank=True)
    source_phone = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

import decimal
import time
import string
import random
import uuid
from django.db import models

# from accounts.models import User


class Agency(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    wallet = models.ForeignKey('Wallet', on_delete=models.CASCADE, null=True, blank=True)  # noqa
    business_certificate = models.ImageField(upload_to="agency_certificate/", null=True, blank=True)  # noqa
    contact_person_ID = models.ImageField(upload_to="user_ID/", null=True, blank=True)  # noqa
    is_approved = models.BooleanField(default=False)
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
    seat_num = models.IntegerField(default=0)
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

    def get_agencies_in_category(self):
        vehicles = Vehicle.objects.filter(category=self)
        agencies = Agency.objects.none()
        for vehicle in vehicles:
            agencies |= Agency.objects.filter(id=vehicle.agency.id)
        return agencies

    def __str__(self):
        return self.name if self.name else "category"

    class Meta:
        db_table = 'category'


class Trip(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True, blank=True)  # noqa
    source = models.CharField(max_length=255, null=True, blank=True)
    destination = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(decimal_places=3, max_digits=10, default=0)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def get_trip_type(self):
        return self.vehicle.category.name if self.vehicle else None

    def __str__(self):
        return self.source + "-" + self.destination if self.source and self.destination else "trip"  # noqa

    class Meta:
        db_table = 'trip'


class Booking(models.Model):
    def generate_ticket_id():
        time_id = str(int(time.time() * 1000))
        return "G".join(random.choices(string.ascii_uppercase + time_id + string.digits, k=6))
    booking_code = models.CharField(max_length=255, default=generate_ticket_id)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=True, blank=True)  # noqa
    seats = models.ManyToManyField(Seat, blank=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, null=True, blank=True)  # noqa
    date = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def get_seat_numbers(self):
        data = self.seats.all()
        seats = ""
        for seat in data:
            seats += str(seat.seat_num) + ", "
        return seats.strip(", ")

    def __str__(self):
        return self.user.email if self.user.email else "booking"

    class Meta:
        db_table = 'booking'


class Ticket(models.Model):
    def generate_ticket_id():
        time_id = str(int(time.time() * 1000))
        return "".join(random.choices(string.ascii_uppercase + time_id + string.digits, k=12))
    ticket_id = models.CharField(max_length=100, default=generate_ticket_id)
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE, null=True, blank=True)  # noqa
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticket_id if self.ticket_id else "ticket"

    class Meta:
        db_table = 'ticket'


class Transaction(models.Model):
    def generate_transaction_id():
        time_id = str(int(time.time() * 100))
        return "".join(random.choices(string.ascii_uppercase + time_id + string.digits, k=12))
    transaction_id = models.CharField(max_length=255, primary_key=True, default=generate_transaction_id)  # noqa
    external_id = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    network = models.CharField(max_length=255, null=True, blank=True)
    status_code = models.CharField(max_length=255, null=True, blank=True)
    status_message = models.CharField(max_length=255, null=True, blank=True)
    source_phone = models.CharField(max_length=255, null=True, blank=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)  # noqa
    note = models.CharField(max_length=255, null=True, blank=True)
    transaction_type = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id if self.transaction_id else "transaction"


class Wallet(models.Model):
    wallet_id = models.CharField(max_length=100, default=uuid.uuid4)
    main_balance = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)  # noqa
    available_balance = models.DecimalField(decimal_places=2, max_digits=50, default=0.0)  # noqa
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def credit_available_balance(self, amount):
        self.available_balance += decimal.Decimal(amount)
        self.save()

    def debit_available_balance(self, amount):
        self.available_balance -= decimal.Decimal(amount)
        self.save()

    def credit_main_balance(self, amount):
        self.main_balance += decimal.Decimal(amount)
        self.save()

    def debit_main_balance(self, amount):
        self.main_balance -= decimal.Decimal(amount)
        self.save()

    def credit_wallet(self, amount):
        self.main_balance += decimal.Decimal(amount)
        self.available_balance += decimal.Decimal(amount)
        self.save()

    def debit_wallet(self, amount):
        self.main_balance -= decimal.Decimal(amount)
        self.available_balance -= decimal.Decimal(amount)
        self.save()

    def get_wallet_balance(self):
        return decimal.Decimal(self.main_balance)

    def __str__(self):
        return self.wallet_id

    class Meta:
        permissions = [
            ("cashout_from_wallet", "Can cashout from wallet"),
        ]

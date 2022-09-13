from email.policy import default
from django.contrib.auth import authenticate
from accounts.models import User
from backend.models import Booking, Transaction, Trip, Seat, Ticket, Agency, VehicleCategory
from rest_framework import serializers
from rest_framework.response import Response


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'


class SearchTripSerializer(serializers.ModelSerializer):
    agency = serializers.IntegerField(write_only=True)
    source = serializers.CharField(allow_null=True, allow_blank=True)  # noqa
    destination = serializers.CharField(allow_null=True, allow_blank=True)  # noqa
    date = serializers.DateField()  # noqa

    class Meta:
        model = Trip
        fields = '__all__'


class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(write_only=True)
    trip = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    network = serializers.CharField(max_length=20, default='MTN')
    source_phone = serializers.CharField(max_length=15, allow_blank=True)
    amount = serializers.DecimalField(
        decimal_places=3, max_digits=10)
    note = serializers.CharField(max_length=500, default="Payment for trip")

    class Meta:
        model = Transaction
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return Response(user, status=200)
        raise Response(
            {"error": "Unable to log in with provided credentials."}, status=400)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'], password=validated_data['password'], first_name=validated_data['first_name'], last_name=validated_data['last_name'])
        return user


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleCategory
        exclude = ["date_created"]

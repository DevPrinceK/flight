from django.core import serializers
import json
from accounts.models import User
import time
from core import settings
from backend.models import Booking, Seat, Transaction, Trip
from django.shortcuts import render
from django.views import View
from api.serializers import BookingSerializer, RegisterSerializer, TripSerializer, UserSerializer
from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login


class HomeAPIView(APIView):
    '''endpoint for all endpoints'''

    def get(self, request, *args, **kwargs):
        end_points = {
            'login': '/api/login/',
            'sign-up': '/api/sign-up/',
            'all-trips': '/api/all-trips/',
            'trips-today': '/api/trips-today/',
            'custom-trips': '/api/custom-trips/',
            'bookings': '/api/bookings/',
            'book-trip': '/api/book-trip/',
        }
        return Response(end_points)


class AllTripsAPI(APIView):
    '''endpoint for getting all trips available'''
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        trips = Trip.objects.all()
        print(trips)
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)


class TripsTodayAPI(APIView):
    '''endpoint for getting all trips for the day'''
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        trips = Trip.objects.filter(date=time.strftime("%Y-%m-%d"))
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)


class CustomTripsAPI(APIView):
    '''endpoint for getting all trips for the day'''
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        print(request.data)
        source = request.data['source']
        destination = request.data['destination']
        # date format: YYYY-MM-DD
        date = request.data['date']
        trips = Trip.objects.filter(date=date, source=source, destination=destination)  # noqa
        serializer = TripSerializer(trips, many=True)
        if trips:
            return Response(serializer.data)
        else:
            return Response({"error": "No trips found for your source and destination"}, status=status.HTTP_404_NOT_FOUND)  # noqa


class BookTripAPI(APIView):
    '''endpoint to book trips'''
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        trip_id = request.data['trip']
        user_id = request.data['user']
        seat_id = request.data['seat']
        trip = Trip.objects.filter(id=int(trip_id)).first()
        user = User.objects.filter(id=int(user_id)).first()
        seat = Seat.objects.filter(id=int(seat_id)).first()
        booking = Booking.objects.create(seat=seat, user=user, trip=trip)
        serialized = serializers.serialize(queryset=[booking], format='json')
        return Response({"booking": serialized}, status=status.HTTP_201_CREATED)


class LoginAPI(KnoxLoginView):
    '''Login api endpoint'''
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class SignUpAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1]
        })

from unicodedata import decimal
from django.core import serializers
import json
from accounts.models import User
import time
from core import settings
from backend.models import Agency, Booking, Seat, Transaction, Trip, Vehicle, Ticket
from django.shortcuts import render
from django.views import View
from api.serializers import BookingSerializer, PaymentSerializer, RegisterSerializer, SeatSerializer, TripSerializer, UserSerializer, TicketSerializer, AgencySerializer  # noqa
from core.utils.util_functions import get_transaction_status, receive_payment
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


class OverviewAPI(APIView):
    '''endpoint for all endpoints'''

    def get(self, request, *args, **kwargs):
        end_points = {
            'overview': '/api/',
            'login': '/api/login/',
            'sign-up': '/api/sign-up/',
            'all-trips': '/api/all-trips/',
            'trips-today': '/api/trips-today/',
            'search-trips': '/api/search-trips/',
            'bookings': '/api/bookings/',
            'book-trip': '/api/book-trip/',
            'pay-for-trip': '/api/pay-for-trip/',
            'user-bookings': '/api/user-bookings/',
            'get-vehicle-seats': '/api/get-vehicle-seats/',
            'user-tickets': '/api/user-tickets/',
            'user-profile': '/api/user-profile/',
            'all-agencies': '/api/all-agencies/',
        }
        return Response(end_points)


class UserProfileAPI(APIView):
    '''endpoint for getting user details from a given token'''
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        # extract token key from user tokenand use it to find the user
        token = request.data.get('token')
        try:
            # token_str = request.META.get(
            #     'HTTP_AUTHORIZATION').split(' ')[1][0:8]
            token_str = token[0:8]
        except AttributeError:
            return Response({'error': 'No token found'})
        user = AuthToken.objects.filter(
            token_key=token_str).first().user
        serializer = UserSerializer(user, many=False)
        return Response({"user": serializer.data})


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


class SearchTripsAPI(APIView):
    '''endpoint for getting all trips for the day'''
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # agency_id = request.data['agency']
        # source = request.data['source']
        # destination = request.data['destination']
        agency_id = request.data.get('agency')
        source = request.data.get('source')
        destination = request.data.get('destination')
        agency = Agency.objects.filter(id=int(agency_id)).first()
        # date format: YYYY-MM-DD
        # date = request.data['date']
        date = request.data.get('date')
        trips = Trip.objects.filter(date=date, source=source, destination=destination, vehicle__agency=agency)  # noqa
        serializer = TripSerializer(trips, many=True)
        if trips:
            return Response(serializer.data)
        else:
            return Response({"error": "No trips found for your search query"}, status=status.HTTP_404_NOT_FOUND)  # noqa


class BookTripAPI(APIView):
    '''endpoint to book trips'''
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        trip_id = request.data['trip']
        user_id = request.data['user']
        seat_ids = request.data['seats']
        trip = Trip.objects.filter(id=int(trip_id)).first()
        user = User.objects.filter(id=int(user_id)).first()
        # seat = Seat.objects.filter(id=int(seat_id)).first()
        booking = Booking.objects.create(user=user, trip=trip)
        booking.save()
        for seat_id in seat_ids:
            try:
                seat = Seat.objects.filter(id=int(seat_id)).first()
                booking.seats.add(seat)
                booking.save()
                seat.is_booked = True
                seat.save()
            except Exception as e:
                booking.delete()
                return Response({"error": e}, status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.serialize(queryset=[booking], format='json')
        return Response({"booking": serialized}, status=status.HTTP_201_CREATED)


class UserBookings(APIView):
    '''endpoint to get all trips booked by the user'''
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        user_id = request.data['user']
        user = User.objects.filter(id=int(user_id)).first()
        bookings = Booking.objects.filter(user=user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)


class VehicleSeatsAPI(APIView):
    '''endpoint for getting the seats for a particular vehicle'''
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        vehicle_id = request.data['vehicle']
        vehicle = Vehicle.objects.filter(id=int(vehicle_id)).first()
        seats = Seat.objects.filter(vehicle=vehicle)
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data)


class UserTicketsAPI(APIView):
    '''endpoint for getting the tickets for a particular user'''
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user_id = request.data['user']
        user = User.objects.filter(id=int(user_id)).first()
        tickets = Ticket.objects.filter(transaction__booking__user=user)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)


class AllAgenciesAPI(APIView):
    '''endpoint for getting all agencies'''
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        agencies = Agency.objects.all()
        serializer = AgencySerializer(agencies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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


class PayForTripAPI(APIView):
    def generate_transaction_id(self):
        return int(round(time.time() * 10000))

    def post(self, request, *args, **kwargs):
        booking_id = request.data['booking']
        serializer = PaymentSerializer(data=request.data)
        # get the particular booking
        booking = Booking.objects.filter(id=int(booking_id)).first()

        if serializer.is_valid():
            serializer.save()
            transaction_id = self.generate_transaction_id()
            data = {
                'transaction_id': transaction_id,
                'mobile_number': serializer['source_phone'].value,
                'amount': serializer['amount'].value,
                'wallet_id': settings.PAYHUB_WALLET_ID,
                'network_code': serializer['network'].value,
                'note': 'Payment for booking service',
            }
            # initiate payment
            receive_payment(data)

            transaction_is_successful = False
            for i in range(5):
                time.sleep(5)
                transaction_status = get_transaction_status(transaction_id)  # noqa
                print(transaction_status)
                if transaction_status['success'] == True:
                    transaction_is_successful = True
                    print('the transaction was successful')
                    break

            transaction = {
                'transaction_id': transaction_id,
                'external_id': "",
                'amount': serializer['amount'].value,
                'source_phone': serializer['source_phone'].value,
                'network': serializer['network'].value,
                'note': 'Payment for booking service',
                'status_code': transaction_status['status_code'],
                'status_message': transaction_status['message'],
                'booking': booking,
                'transaction_type': "CashIn",
            }
            print("Saving Transaction")
            Transaction.objects.create(**transaction)
            # credit agency account if transaction is successful
            if transaction_is_successful:
                try:
                    # credit agency wallet with 95% of amount
                    agency_amount = 0.95 * decimal.Decimal(serializer['amount'].value)  # noqa
                    booking.trip.vehicle.agency.wallet.credit_wallet(decimal.Decimal(agency_amount))  # noqa
                    print(f"AGENCY ACCOUNT CREDITED WITH {agency_amount}")
                except Exception as e:
                    print(e)
            print('Transaction Saved')
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        # if transaction data is not valid
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

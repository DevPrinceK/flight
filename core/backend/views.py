from django.shortcuts import render
from django.views import View

from backend.models import Vehicle
from backend.models import Transaction
from backend.models import Booking
from backend.models import Ticket
from backend.models import Seat
from backend.models import Trip
from backend.models import VehicleCategory


class DashboardView(View):
    template = "backend/index.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template, context)


class VehicleListView(View):
    template = "backend/lists/vehicles.html"

    def get(self, request, *args, **kwargs):
        vehicles = Vehicle.objects.all().order_by('-id')
        context = {'vehicles': vehicles}
        return render(request, self.template, context)


class TransactionListView(View):
    template = "backend/lists/transactions.html"

    def get(self, request, *args, **kwargs):
        transactions = Transaction.objects.all().order_by('-id')
        context = {'transactions': transactions}
        return render(request, self.template, context)


class BookingListView(View):
    template = "backend/lists/bookings.html"

    def get(self, request, *args, **kwargs):
        bookings = Booking.objects.all().order_by('-id')
        context = {'bookings': bookings}
        return render(request, self.template, context)


class TicketListView(View):
    template = "backend/lists/tickets.html"

    def get(self, request, *args, **kwargs):
        tickets = Ticket.objects.all().order_by('-id')
        context = {'tickets': tickets}
        return render(request, self.template, context)


class SeatListView(View):
    template = "backend/lists/seats.html"

    def get(self, request, *args, **kwargs):
        seats = Seat.objects.all().order_by('-id')
        context = {'seats': seats}
        return render(request, self.template, context)


class TripListView(View):
    template = "backend/lists/trips.html"

    def get(self, request, *args, **kwargs):
        trips = Trip.objects.all().order_by('-id')
        context = {'trips': trips}
        return render(request, self.template, context)


class CategoryListView(View):
    template = "backend/lists/categories.html"

    def get(self, request, *args, **kwargs):
        categories = VehicleCategory.objects.all().order_by('-id')
        context = {'categories': categories}
        return render(request, self.template, context)

from django.shortcuts import render
from django.views import View
from backend.models import Booking

class BookingListView(View):
    template = "backend/lists/bookings.html"

    def get(self, request, *args, **kwargs):
        bookings = Booking.objects.all().order_by('-id')
        context = {'bookings': bookings}
        return render(request, self.template, context)

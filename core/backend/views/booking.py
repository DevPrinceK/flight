from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from backend.models import Booking

from core.utils.decorators import MustLogin


class BookingListView(View):
    permission_required = [
        "backend.view_booking",
    ]
    template = "backend/lists/bookings.html"

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            bookings = Booking.objects.all().order_by('-id')
        elif request.user.is_agency_admin:
            bookings = Booking.objects.filter(
                trip__vehicle__agency=request.user.agency)
        context = {'bookings': bookings}
        return render(request, self.template, context)

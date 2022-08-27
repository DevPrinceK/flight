from django.shortcuts import render
from django.views import View
from backend.models import Seat


class SeatListView(View):
    template = "backend/lists/seats.html"

    def get(self, request, *args, **kwargs):
        seats = Seat.objects.all().order_by('-id')
        context = {'seats': seats}
        return render(request, self.template, context)

from django.shortcuts import render
from django.views import View
from backend.models import Trip


class TripListView(View):
    template = "backend/lists/trips.html"

    def get(self, request, *args, **kwargs):
        trips = Trip.objects.all().order_by('-id')
        context = {'trips': trips}
        return render(request, self.template, context)
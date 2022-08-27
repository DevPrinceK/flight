from django.shortcuts import render
from django.views import View

from backend.models import Vehicle


class VehicleListView(View):
    template = "backend/lists/vehicles.html"

    def get(self, request, *args, **kwargs):
        vehicles = Vehicle.objects.all().order_by('-id')
        context = {'vehicles': vehicles}
        return render(request, self.template, context)

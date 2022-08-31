from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.utils.html import strip_tags
from django.utils.decorators import method_decorator
from core.utils.decorators import MustLogin
from backend.forms import TripForm

from backend.models import Trip, Vehicle


class TripListView(PermissionRequiredMixin, View):
    permission_required = [
        "backend.view_trip",
    ]
    template = "backend/lists/trips.html"

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            trips = Trip.objects.all().order_by('-id')
        elif request.user.is_agency_admin:
            trips = Trip.objects.filter(vehicle__agency=request.user.agency)  # noqa
        context = {'trips': trips}
        return render(request, self.template, context)


class CreateUpdateTrip(PermissionRequiredMixin, View):
    permission_required = [
        "backend.add_trip",
        "backend.change_trip",
    ]
    template = "backend/create_update_trip.html"

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        trip_id = request.GET.get('trip_id')
        vehicle_id = request.GET.get('vehicle_id')
        if request.user.is_staff or request.user.is_superuser:
            trip = Trip.objects.filter(id=trip_id).first()
            vehicle = Vehicle.objects.filter(id=vehicle_id).first()
            vehicles = Vehicle.objects.all()
        elif request.user.is_agency_admin:
            trip = Trip.objects.filter(id=trip_id, vehicle__agency=request.user.agency).first()  # noqa
            vehicle = Vehicle.objects.filter(id=vehicle_id, agency=request.user.agency).first()  # noqa
            vehicles = Vehicle.objects.filter(agency=request.user.agency)
        else:
            vehicles = {}
        context = {
            "vehicle": vehicle,
            "vehicles": vehicles,
            "trip": trip,
        }  # noqa
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        trip_id = request.POST.get('trip_id')
        vehicle_id = request.POST.get('vehicle_id')
        if request.user.is_staff or request.user.is_superuser:
            vehicle = Vehicle.objects.filter(id=vehicle_id).first()
        elif request.user.is_agency_admin:
            vehicle = Vehicle.objects.filter(id=vehicle_id, agency=request.user.agency).first()  # noqa
        if trip_id:
            # trip exists - update trip
            if request.user.is_staff or request.user.is_superuser:
                trip = Trip.objects.filter(id=trip_id).first()
            elif request.user.is_agency_admin:
                trip = Trip.objects.filter(id=trip_id, vehicle__agency=request.user.agency).first()  # noqa

            form = TripForm(request.POST, request.FILES, instance=trip)  # noqa
            if form.is_valid():
                new_trip = form.save(commit=False)
                new_trip.vehicle = vehicle
                new_trip.save()
                messages.success(request, 'Trip Detail Updated Successfully.')  # noqa
                return redirect('backend:trips')
            else:
                for field, error in form.errors.items():
                    message = f"{field.title()}: {strip_tags(error)}"
                    break
                messages.warning(request, message)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            # it's a new trip - create trip
            form = TripForm(request.POST, request.FILES)
            if form.is_valid():
                seat = form.save(commit=False)
                seat.vehicle = vehicle
                seat.save()
                messages.success(request, 'New Trip Created Successfully.')  # noqa
                return redirect('backend:trips')
            else:
                for field, error in form.errors.items():
                    message = f"{field.title()}: {strip_tags(error)}"
                    break
                messages.warning(request, message)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class DeleteTrip(PermissionRequiredMixin, View):
    permission_required = [
        "backend.delete_trip",
    ]

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        return redirect('backend:trips')

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        trip_id = request.POST.get('trip_id')
        if request.user.is_staff or request.user.is_superuser:
            trip = Trip.objects.filter(id=trip_id).first()
        elif request.user.is_agency_admin:
            trip = Trip.objects.filter(id=trip_id, vehicle__agency=request.user.agency).first()  # noqa
        trip.delete()
        messages.success(request, 'Trip Deleted Successfully.')
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
